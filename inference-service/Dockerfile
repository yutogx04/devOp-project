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

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code and model
COPY app/ ./app/
COPY model/ ./model/

# Environment defaults
ENV MODEL_PATH=/app/model/model.joblib \
    MODEL_VERSION=1.0.0

# Switch to non-root user
USER appuser

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
