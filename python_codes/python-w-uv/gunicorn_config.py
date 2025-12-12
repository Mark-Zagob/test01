import multiprocessing
import os

# Bind
bind = "0.0.0.0:5000"

# Workers
# Công thức: (2 x CPU cores) + 1
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'  # hoặc 'gevent' cho async
worker_connections = 1000
max_requests = 1000  # Restart worker sau N requests (tránh memory leak)
max_requests_jitter = 50  # Random jitter để tránh restart cùng lúc
timeout = 30  # Worker timeout (seconds)
keepalive = 2

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stdout
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Preload app để tiết kiệm memory
preload_app = True

# Graceful timeout
graceful_timeout = 30

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Process naming
proc_name = 'myapp'

# Server hooks (optional)
def on_starting(server):
    server.log.info("Gunicorn server starting")

def on_reload(server):
    server.log.info("Gunicorn server reloading")

def when_ready(server):
    server.log.info("Gunicorn server ready")

def on_exit(server):
    server.log.info("Gunicorn server shutting down")