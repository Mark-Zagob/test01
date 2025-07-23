import logging
from flask import Flask, jsonify

# Khởi tạo Flask app
app = Flask(__name__)

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,  # Mức độ log (DEBUG, INFO, WARNING, ERROR)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Tạo logger riêng
logger = logging.getLogger(__name__)

@app.route('/')
def hello_world():
    logger.info("Truy cập endpoint /")
    return jsonify(message='Hello World!')

@app.route('/error')
def trigger_error():
    logger.error("Đã xảy ra lỗi mẫu!")
    return jsonify(error="This is a sample error"), 500