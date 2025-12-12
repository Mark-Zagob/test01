import multiprocessing
import os

# Bind
bind = "0.0.0.0:5000"

# Workers - Tối ưu cho container
# Trong container nên dùng công thức nhẹ hơn: (CPU cores * 2) hoặc min(CPU*2+1, 4)
cpu_count = multiprocessing.cpu_count()
default_workers = min(cpu_count * 2 + 1, 4)  # Giới hạn tối đa 4 workers
workers = int(os.getenv('GUNICORN_WORKERS', default_workers))

# Worker class
worker_class = os.getenv('WORKER_CLASS', 'sync')  # sync, gevent, gthread
threads = int(os.getenv('THREADS', 1))  # Cho gthread worker
worker_connections = 1000

# Worker lifecycle
max_requests = int(os.getenv('MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('MAX_REQUESTS_JITTER', 50))
timeout = int(os.getenv('TIMEOUT', 30))
keepalive = int(os.getenv('KEEPALIVE', 2))
graceful_timeout = int(os.getenv('GRACEFUL_TIMEOUT', 30))

# Logging
accesslog = os.getenv('ACCESS_LOG', '-')  # stdout
errorlog = os.getenv('ERROR_LOG', '-')    # stdout
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Disable access log nếu muốn giảm noise (chỉ dùng Flask logging)
# accesslog = None
# disable_redirect_access_to_syslog = True

# Performance
preload_app = True  # Load app trước khi fork workers (tiết kiệm RAM)
worker_tmp_dir = '/dev/shm'  # Dùng shared memory cho heartbeat (nhanh hơn disk)

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Process naming
proc_name = os.getenv('PROC_NAME', 'myapp')

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info(f"Starting Gunicorn {server.cfg.proc_name}")
    server.log.info(f"Workers: {server.cfg.workers}, Worker class: {server.cfg.worker_class}")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading Gunicorn")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Gunicorn is ready. Spawning workers")

def worker_int(worker):
    """Called when a worker receives the SIGINT or SIGQUIT signal."""
    worker.log.info(f"Worker {worker.pid} received SIGINT/SIGQUIT")

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    worker.log.warning(f"Worker {worker.pid} received SIGABRT (timeout?)")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forking new master process")

def worker_exit(server, worker):
    """Called just after a worker has been exited."""
    server.log.info(f"Worker exited (pid: {worker.pid})")

def on_exit(server):
    """Called just before exiting Gunicorn."""
    server.log.info("Shutting down Gunicorn")