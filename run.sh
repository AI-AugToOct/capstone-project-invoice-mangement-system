#!/bin/bash

echo "============================================"
echo "📊 مُـفـــــوْتِــــر - Smart Invoice Analyzer"
echo "============================================"
echo ""
echo "🚀 Starting Backend (FastAPI) + Frontend (Next.js)..."
echo ""

# 🔹 Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv"
    exit 1
fi

# 🔹 Activate virtual environment
source venv/bin/activate

# 🔹 Set PYTHONPATH to current directory
export PYTHONPATH=$(pwd)

# 🔹 Start FastAPI backend in new terminal
echo "🔧 Starting Backend Server (Port 8000)..."

# Check if running on macOS (use osascript) or Linux (use gnome-terminal/xterm)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal"
        do script "cd '"$(pwd)"' && source venv/bin/activate && python -m uvicorn backend.main:app --reload --port 8000"
    end tell' > /dev/null 2>&1
elif command -v gnome-terminal &> /dev/null; then
    # Linux with GNOME
    gnome-terminal -- bash -c "cd $(pwd) && source venv/bin/activate && python -m uvicorn backend.main:app --reload --port 8000; exec bash"
elif command -v xterm &> /dev/null; then
    # Linux with xterm
    xterm -e "cd $(pwd) && source venv/bin/activate && python -m uvicorn backend.main:app --reload --port 8000" &
else
    # Fallback: run in background
    python -m uvicorn backend.main:app --reload --port 8000 &
    BACKEND_PID=$!
fi

# 🔹 Wait 3 seconds for backend to start
sleep 3

# 🔹 Check if node_modules exists in frontend-nextjs
if [ ! -d "frontend-nextjs/node_modules" ]; then
    echo ""
    echo "⚠️  Frontend dependencies not installed!"
    echo "📦 Installing dependencies... (this may take a few minutes)"
    cd frontend-nextjs
    npm install
    cd ..
fi

# 🔹 Start Next.js frontend in new terminal
echo "🎨 Starting Frontend Server (Port 3000)..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal"
        do script "cd '"$(pwd)/frontend-nextjs"' && npm run dev"
    end tell' > /dev/null 2>&1
elif command -v gnome-terminal &> /dev/null; then
    # Linux with GNOME
    gnome-terminal -- bash -c "cd $(pwd)/frontend-nextjs && npm run dev; exec bash"
elif command -v xterm &> /dev/null; then
    # Linux with xterm
    xterm -e "cd $(pwd)/frontend-nextjs && npm run dev" &
else
    # Fallback: run in background
    cd frontend-nextjs
    npm run dev &
    FRONTEND_PID=$!
    cd ..
fi

# 🔹 Wait 5 seconds for frontend to start
sleep 5

echo ""
echo "============================================"
echo "✅ Servers Started Successfully!"
echo "============================================"
echo ""
echo "📍 Backend API:  http://127.0.0.1:8000"
echo "📍 API Docs:     http://127.0.0.1:8000/docs"
echo "📍 Frontend UI:  http://localhost:3000"
echo ""
echo "⚠️  To stop servers:"
echo "   - Close terminal windows (macOS/Linux GUI)"
echo "   - Or press Ctrl+C in each terminal"
echo "============================================"
echo ""

# Keep script running
wait
