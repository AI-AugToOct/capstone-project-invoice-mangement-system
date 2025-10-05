#!/bin/bash
echo "--------------------------------------------"
echo "📦 Starting Smart Invoice Analyzer"
echo "--------------------------------------------"

# 🔹 Activate virtual environment
source venv/bin/activate

# 🔹 Set PYTHONPATH to current directory (fix import issue)
export PYTHONPATH=$(pwd)

# 🔹 Start FastAPI backend from root (in background)
osascript -e 'tell app "Terminal"
    do script "cd '$(pwd)' && source venv/bin/activate && python -m uvicorn backend.main:app --reload --port 8000"
end tell'

# 🔹 Wait 5 seconds for backend to start
sleep 5

# 🔹 Start Streamlit frontend
cd frontend
streamlit run app.py
