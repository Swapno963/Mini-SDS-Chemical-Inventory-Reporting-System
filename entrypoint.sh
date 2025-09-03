#!/bin/sh
set -e

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start FastAPI app
echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
