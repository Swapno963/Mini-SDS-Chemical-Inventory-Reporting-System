FROM python:3.10-slim AS builder
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt





FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH


# Install just postgres client
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*


# Copy application code
COPY alembic.ini .
COPY migrations/ migrations/
COPY app/ app/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run the application 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


