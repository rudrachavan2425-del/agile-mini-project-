# =========================================================================
# Multi-Stage / Lightweight Production Dockerfile for Online Placement System
# =========================================================================

FROM python:3.12-slim AS base

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create non-root user for security best practices
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# Healthcheck configuration for Docker & Orchestration
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose port for Flask WSGI server
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
