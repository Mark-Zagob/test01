# syntax=docker/dockerfile:1.19

# ============ Stage 1: Dependencies ============
FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy dependency files (tận dụng layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies vào virtual environment
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# ============ Stage 2: Runtime ============
FROM python:3.11-slim

# Tạo non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy virtual environment từ builder (thay vì copy system packages)
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

EXPOSE 5000

# Thêm venv vào PATH để dùng Python và packages từ venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
