#!/bin/sh
set -e



# Wait for Postgres to be ready
echo "Waiting for Postgres to start..."
echo "DB_HOST: $DB_HOST"
echo "DB_PORT: $DB_PORT"
echo "DB_USER: $DB_USER"
export PGPASSWORD=$DB_PASSWORD

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" ; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done



# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
