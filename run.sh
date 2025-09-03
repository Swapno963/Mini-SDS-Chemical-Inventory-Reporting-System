#!/bin/bash

set -e



echo "Starting the FastAPI application."
sudo docker-compose up --build

echo "Waiting for postgres to be ready."


echo "Running Alembic migrations."