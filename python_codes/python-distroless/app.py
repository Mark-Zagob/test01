import logging
from flask import Flask, jsonify, request
from config import get_config
import os

# Khởi tạo Flask app
app = Flask(__name__)

# Load configuration từ config.py
app.config.from_object(get_config())

# Cấu hình logging
def setup_logging():
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    
    return logging.getLogger(__name__)

logger = setup_logging()

# Request logging middleware
@app.before_request
def log_request_info():
    # Bỏ qua health check để tránh spam logs
    if request.path in ['/health', '/ready']:
        return
    logger.info(f'{request.method} {request.path} - IP: {request.remote_addr}')

@app.after_request
def log_response_info(response):
    # Bỏ qua health check
    if request.path in ['/health', '/ready']:
        return response
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
    return jsonify(
        message='Test, Merge',
        version='0.1.0',
        environment=os.getenv('FLASK_ENV', 'production')
    )

@app.route('/health')
def health():
    """Health check endpoint for Docker"""
    return '', 200  # Trả về empty response cho healthcheck nhanh hơn

@app.route('/ready')
def ready():
    """Readiness probe - check if app can handle requests"""
    try:
        # Có thể thêm logic kiểm tra database, cache, etc.
        # Example: db.session.execute('SELECT 1')
        return '', 200
    except Exception as e:
        logger.error(f'Readiness check failed: {str(e)}')
        return '', 503

@app.route('/error')
def trigger_error():
    logger.error("Đã xảy ra lỗi mẫu!")
    return jsonify(error="This is a sample error"), 500

if __name__ == '__main__':
    # Only for development
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])