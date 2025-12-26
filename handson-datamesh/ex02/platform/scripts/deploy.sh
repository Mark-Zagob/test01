#!/bin/bash

# ============================================================
# DATA PRODUCT DEPLOY SCRIPT
# Script này deploy một data product đã được validate
# ============================================================

set -e  # Exit ngay nếu có lỗi

# ---------------------------
# CONFIGURATION
# ---------------------------

SCHEMA_REGISTRY_URL="${SCHEMA_REGISTRY_URL:-http://localhost:8081}"
KAFKA_BOOTSTRAP_SERVER="${KAFKA_BOOTSTRAP_SERVER:-localhost:9092}"
MINIO_ALIAS="${MINIO_ALIAS:-myminio}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ---------------------------
# HELPER FUNCTIONS
# ---------------------------

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# ---------------------------
# DEPLOY FUNCTIONS
# ---------------------------

read_dataproduct_config() {
    log_step "Reading dataproduct.yaml..."
    
    local yaml_file="$DATA_PRODUCT_PATH/dataproduct.yaml"
    
    # Extract values from dataproduct.yaml
    DP_NAME=$(yq eval '.metadata.name' "$yaml_file")
    DP_DOMAIN=$(yq eval '.metadata.domain' "$yaml_file")
    DP_VERSION=$(yq eval '.metadata.version' "$yaml_file")
    
    log_info "Data Product: $DP_NAME"
    log_info "Domain: $DP_DOMAIN"
    log_info "Version: $DP_VERSION"
}

deploy_schema() {
    log_step "Registering schema to Schema Registry..."
    
    local schema_file="$DATA_PRODUCT_PATH/schema/schema.avsc"
    
    # Get Kafka topic from output config
    local kafka_topic=$(yq eval '.spec.output[] | select(.type == "kafka-topic") | .target' "$DATA_PRODUCT_PATH/dataproduct.yaml")
    
    if [[ -z "$kafka_topic" || "$kafka_topic" == "null" ]]; then
        log_warn "No Kafka topic defined, skipping schema registration"
        return 0
    fi
    
    local subject="${kafka_topic}-value"
    
    log_info "Subject: $subject"
    
    # Check if subject already exists
    local existing=$(curl -s -o /dev/null -w "%{http_code}" "$SCHEMA_REGISTRY_URL/subjects/$subject/versions")
    
    if [[ "$existing" == "200" ]]; then
        log_warn "Subject $subject already exists, checking compatibility..."
    fi
    
    # Register schema
    local response=$(jq -n --slurpfile schema "$schema_file" \
        '{schemaType: "AVRO", schema: ($schema[0] | tostring)}' | \
        curl -s -X POST "$SCHEMA_REGISTRY_URL/subjects/$subject/versions" \
        -H "Content-Type: application/vnd.schemaregistry.v1+json" \
        -d @-)
    
    # Check response
    if echo "$response" | jq -e '.id' > /dev/null 2>&1; then
        local schema_id=$(echo "$response" | jq -r '.id')
        log_info "Schema registered successfully with ID: $schema_id ✓"
    else
        log_error "Failed to register schema: $response"
        return 1
    fi
}

deploy_kafka_topic() {
    log_step "Creating Kafka topic..."
    
    # Get Kafka topic from output config
    local kafka_topic=$(yq eval '.spec.output[] | select(.type == "kafka-topic") | .target' "$DATA_PRODUCT_PATH/dataproduct.yaml")
    
    if [[ -z "$kafka_topic" || "$kafka_topic" == "null" ]]; then
        log_warn "No Kafka topic defined, skipping"
        return 0
    fi
    
    log_info "Topic: $kafka_topic"
    
    # Check if topic already exists
    local existing=$(docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list | grep -w "$kafka_topic" || true)
    
    if [[ -n "$existing" ]]; then
        log_warn "Topic $kafka_topic already exists, skipping creation"
        return 0
    fi
    
    # Create topic
    docker exec kafka kafka-topics --bootstrap-server localhost:9092 \
        --create \
        --topic "$kafka_topic" \
        --partitions 3 \
        --replication-factor 1
    
    log_info "Kafka topic created successfully ✓"
}

deploy_minio_bucket() {
    log_step "Creating MinIO bucket/folder..."
    
    # Get S3 path from output config
    local s3_path=$(yq eval '.spec.output[] | select(.type == "s3") | .target' "$DATA_PRODUCT_PATH/dataproduct.yaml")
    
    if [[ -z "$s3_path" || "$s3_path" == "null" ]]; then
        log_warn "No S3 output defined, skipping"
        return 0
    fi
    
    log_info "S3 Path: $s3_path"
    
    # Extract bucket and path from s3://bucket/path/
    # Remove s3:// prefix
    local path_without_prefix="${s3_path#s3://}"
    
    # Extract bucket name (first part)
    local bucket_name=$(echo "$path_without_prefix" | cut -d'/' -f1)
    
    # Extract folder path (rest)
    local folder_path=$(echo "$path_without_prefix" | cut -d'/' -f2-)
    
    log_info "Bucket: $bucket_name"
    log_info "Folder: $folder_path"
    
    # Create bucket if not exists
    if ! mc ls "$MINIO_ALIAS/$bucket_name" > /dev/null 2>&1; then
        mc mb "$MINIO_ALIAS/$bucket_name"
        log_info "Bucket $bucket_name created ✓"
    else
        log_warn "Bucket $bucket_name already exists"
    fi
    
    # Create folder structure
    # MinIO creates folders automatically when you put an object
    # We'll create a .keep file to ensure folder exists
    echo "Placeholder file to maintain folder structure" | mc pipe "$MINIO_ALIAS/$bucket_name/$folder_path/.keep"
    
    log_info "Folder structure created ✓"
}

# ---------------------------
# MAIN
# ---------------------------

main() {
    # Check argument
    if [[ -z "$1" ]]; then
        echo "Usage: $0 <path-to-data-product>"
        echo "Example: $0 domains/orders/orders-completed"
        exit 1
    fi
    
    DATA_PRODUCT_PATH="$1"
    
    # Check if path exists
    if [[ ! -d "$DATA_PRODUCT_PATH" ]]; then
        log_error "Data product path not found: $DATA_PRODUCT_PATH"
        exit 1
    fi
    
    echo ""
    echo "=========================================="
    echo "Deploying Data Product: $DATA_PRODUCT_PATH"
    echo "=========================================="
    echo ""
    
    # Run deployment steps
    read_dataproduct_config
    echo ""
    deploy_schema
    echo ""
    deploy_kafka_topic
    echo ""
    deploy_minio_bucket
    
    echo ""
    log_info "=========================================="
    log_info "Deployment completed successfully! ✓"
    log_info "=========================================="
    echo ""
}

main "$@"
