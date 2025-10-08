
PORT=8080
echo "PORT env variable: $PORT"
echo "PORT with default: ${PORT:-8000}"

if [ -z "$PORT" ]; then
    echo "PORT not set, using default 8000"
    PORT=8000
else
    echo "PORT is set to: $PORT"
fi

echo "Final PORT value: $PORT"
echo "Command would be: uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
