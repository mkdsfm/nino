#!/bin/sh

set -e

# Run database initialization
echo "Initializing database..."
python -m app.init_db

# Start the application
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
