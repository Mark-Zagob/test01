# ============ Stage 1: Builder ============
FROM python:3.11-slim AS builder

WORKDIR /build

# Cài build dependencies nếu cần (ví dụ: gcc cho psycopg2)
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        gcc \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements và build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ============ Stage 2: Runtime ============
FROM python:3.11-slim

# Tạo non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy wheels từ builder stage và install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && \
    rm -rf /wheels /root/.cache/pip

# Copy source code
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]