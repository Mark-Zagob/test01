# syntax=docker/dockerfile:1

# ============ Stage 1: Builder (Dùng Alpine để build môi trường) ============
FROM python:3.11-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Cài đặt các gói cần thiết để compile thư viện C (nếu cần)
# Nếu app thuần Python thì có thể bỏ dòng RUN apk add này
RUN apk add --no-cache build-base

COPY pyproject.toml uv.lock ./

# Cài đặt dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# ============ Stage 2: Runtime (Alpine sạch) ============
FROM python:3.11-alpine

# Cài lib cần thiết lúc chạy (ví dụ libpq cho postgres nếu cần)
# RUN apk add --no-cache libpq 

RUN addgroup -S appuser && adduser -S appuser -G appuser

WORKDIR /app

# Copy venv từ builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY --chown=appuser:appuser . .

USER appuser

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 5000


CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]