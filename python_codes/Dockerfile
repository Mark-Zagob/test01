FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt 
EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]