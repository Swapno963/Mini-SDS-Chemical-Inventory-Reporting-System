#!/bin/sh
set -e



# Wait for Postgres to be ready
echo "Waiting for Postgres to start..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done



# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
