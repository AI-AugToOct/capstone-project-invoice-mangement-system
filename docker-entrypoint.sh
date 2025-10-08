#!/bin/sh
# Docker entrypoint script for Railway deployment
# Handles PORT environment variable correctly

# Set default port if PORT is not set
PORT=${PORT:-8000}

# Print debug info
echo "🚀 Starting uvicorn on port: $PORT"

# Start uvicorn with the resolved port value
exec uvicorn backend.main:app --host 0.0.0.0 --port "$PORT"

