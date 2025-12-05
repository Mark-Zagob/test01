# gunicorn_config.py
bind = "0.0.0.0:5000"
workers = 2
accesslog = "-"  # Ghi access log ra stdout
errorlog = "-"   # Ghi error log ra stdout
loglevel = "info"