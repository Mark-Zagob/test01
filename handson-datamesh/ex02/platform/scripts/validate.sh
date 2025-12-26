#!/bin/bash

# ============================================================
# DATA PRODUCT VALIDATION SCRIPT
# Script này validate một data product trước khi deploy
# ============================================================

set -e  # Exit ngay nếu có lỗi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# ---------------------------
# VALIDATION FUNCTIONS
# ---------------------------

validate_required_files() {
    log_info "Checking required files..."
    
    local required_files=(
        "dataproduct.yaml"
        "schema/schema.avsc"
        "docs/README.md"
        "quality/expectations.yaml"
    )
    
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$DATA_PRODUCT_PATH/$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        log_error "Missing required files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        return 1
    fi
    
    log_info "All required files present ✓"
    return 0
}

validate_yaml_syntax() {
    log_info "Validating YAML syntax..."
    
    # Check dataproduct.yaml
    if ! yq eval '.' "$DATA_PRODUCT_PATH/dataproduct.yaml" > /dev/null 2>&1; then
        log_error "Invalid YAML syntax in dataproduct.yaml"
        return 1
    fi
    
    # Check expectations.yaml
    if ! yq eval '.' "$DATA_PRODUCT_PATH/quality/expectations.yaml" > /dev/null 2>&1; then
        log_error "Invalid YAML syntax in quality/expectations.yaml"
        return 1
    fi
    
    log_info "YAML syntax valid ✓"
    return 0
}

validate_json_syntax() {
    log_info "Validating JSON syntax..."
    
    # Check schema.avsc
    if ! jq '.' "$DATA_PRODUCT_PATH/schema/schema.avsc" > /dev/null 2>&1; then
        log_error "Invalid JSON syntax in schema/schema.avsc"
        return 1
    fi
    
    log_info "JSON syntax valid ✓"
    return 0
}

validate_dataproduct_fields() {
    log_info "Validating dataproduct.yaml required fields..."
    
    local yaml_file="$DATA_PRODUCT_PATH/dataproduct.yaml"
    
    # Check required fields
    local required_fields=(
        ".metadata.name"
        ".metadata.domain"
        ".metadata.version"
        ".metadata.owner.team"
        ".metadata.owner.email"
        ".spec.description"
        ".spec.output"
        ".spec.sla.freshness"
    )
    
    local missing_fields=()
    
    for field in "${required_fields[@]}"; do
        local value=$(yq eval "$field" "$yaml_file")
        if [[ "$value" == "null" || -z "$value" ]]; then
            missing_fields+=("$field")
        fi
    done
    
    if [[ ${#missing_fields[@]} -gt 0 ]]; then
        log_error "Missing required fields in dataproduct.yaml:"
        for field in "${missing_fields[@]}"; do
            echo "  - $field"
        done
        return 1
    fi
    
    log_info "All required fields present ✓"
    return 0
}

validate_schema_fields() {
    log_info "Validating Avro schema..."
    
    local schema_file="$DATA_PRODUCT_PATH/schema/schema.avsc"
    
    # Check required Avro fields
    local schema_type=$(jq -r '.type' "$schema_file")
    local schema_name=$(jq -r '.name' "$schema_file")
    local schema_fields=$(jq -r '.fields' "$schema_file")
    
    if [[ "$schema_type" != "record" ]]; then
        log_error "Schema type must be 'record', got: $schema_type"
        return 1
    fi
    
    if [[ "$schema_name" == "null" || -z "$schema_name" ]]; then
        log_error "Schema must have a 'name' field"
        return 1
    fi
    
    if [[ "$schema_fields" == "null" ]]; then
        log_error "Schema must have 'fields' array"
        return 1
    fi
    
    log_info "Avro schema valid ✓"
    return 0
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
    echo "Validating Data Product: $DATA_PRODUCT_PATH"
    echo "=========================================="
    echo ""
    
    # Run validations
    validate_required_files || exit 1
    validate_yaml_syntax || exit 1
    validate_json_syntax || exit 1
    validate_dataproduct_fields || exit 1
    validate_schema_fields || exit 1
    
    echo ""
    log_info "=========================================="
    log_info "All validations passed! ✓"
    log_info "=========================================="
    echo ""
}

main "$@"
