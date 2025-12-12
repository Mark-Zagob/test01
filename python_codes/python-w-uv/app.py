import logging
import os
from flask import Flask, jsonify, request
from logging.handlers import RotatingFileHandler

# Khởi tạo Flask app
app = Flask(__name__)

# Configuration từ environment variables
class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
app.config.from_object(Config)

# Cấu hình logging tốt hơn
def setup_logging():
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Configure root logger
    logging.basicConfig(level=log_level, handlers=[console_handler])
    
    return logging.getLogger(__name__)

logger = setup_logging()

# Request logging middleware
@app.before_request
def log_request_info():
    logger.info(f'{request.method} {request.path} - IP: {request.remote_addr}')

@app.after_request
def log_response_info(response):
    logger.info(f'{request.method} {request.path} - Status: {response.status_code}')
    return response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f'404 - {request.path}')
    return jsonify(error='Resource not found'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'500 - {str(error)}')
    return jsonify(error='Internal server error'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception(f'Unhandled exception: {str(e)}')
    return jsonify(error='An unexpected error occurred'), 500

# Routes
@app.route('/')
def hello_world():
    logger.info("Truy cập endpoint /")
    return jsonify(message='Test, Merge', version='0.1.0')

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    return jsonify(status='healthy', service='myapp'), 200

@app.route('/ready')
def ready():
    """Readiness probe - check if app can handle requests"""
    # Có thể thêm logic kiểm tra database, cache, etc.
    return jsonify(status='ready'), 200

@app.route('/error')
def trigger_error():
    logger.error("Đã xảy ra lỗi mẫu!")
    return jsonify(error="This is a sample error"), 500

if __name__ == '__main__':
    # Only for development
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])