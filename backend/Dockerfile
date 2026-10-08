# CSIR Healthcare CDSS Backend Dockerfile
FROM python:3.11-slim as base

# Prevent Python from buffering stdout/stderr and writing bytecode
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application and ML assets
COPY backend/app /app/backend/app
COPY ml/models /app/ml/models
COPY ml/data /app/ml/data
COPY ml/training /app/ml/training
COPY ml/evaluation /app/ml/evaluation
COPY ml/xai /app/ml/xai
COPY ml/__init__.py /app/ml/__init__.py

# Expose FastAPI port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Start Uvicorn server
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
