# ── Stage 1: build dependencies ──────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: production image ───────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="Student3 – Database & Storage Engineer"

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install libpq for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app/ ./app/

# Environment defaults (overridden by docker-compose)
ENV DATABASE_URL=sqlite:///./predictions.db \
    INFERENCE_URL=http://inference-service:8001

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
