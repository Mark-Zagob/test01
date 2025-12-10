# syntax=docker/dockerfile:1

# ============ Stage 1: Builder ============
FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# ============ Stage 2: Runtime (Distroless) ============
FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app

# Copy venv từ builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY --chown=nonroot:nonroot . .

# --- KHẮC PHỤC Ở ĐÂY ---

# 1. Thay vì dùng bin/gunicorn, ta trỏ thẳng vào site-packages để Python nhận diện thư viện
# Lưu ý: Phải đúng version python (3.11)
ENV PYTHONPATH="/app/.venv/lib/python3.11/site-packages"

# 2. Chạy gunicorn bằng cách gọi module (-m) thông qua trình thông dịch Python của hệ thống
# Distroless đã có sẵn python trong path
ENTRYPOINT ["python", "-m", "gunicorn", "--config", "gunicorn_config.py", "app:app"]
