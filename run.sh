#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================"
echo "📑 Smart Invoice Analyzer - Full Stack Starter"
echo "============================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Docker
if command_exists docker && command_exists docker-compose; then
    echo -e "${BLUE}🐳 Docker detected. Choose startup mode:${NC}"
    echo "1) Run with Docker (recommended for production-like environment)"
    echo "2) Run locally (development mode)"
    read -p "Enter choice [1-2]: " choice
    
    if [ "$choice" = "1" ]; then
        echo -e "${GREEN}🐳 Starting with Docker...${NC}"
        
        # Stop any existing containers
        echo "🧹 Cleaning up old containers..."
        docker-compose down 2>/dev/null
        
        # Build and start containers
        echo "🔨 Building Docker images..."
        docker-compose build
        
        echo "🚀 Starting containers..."
        docker-compose up -d
        
        echo ""
        echo -e "${GREEN}✅ Docker containers started successfully!${NC}"
        echo "============================================"
        echo "📍 Backend API:  http://localhost:8000"
        echo "📍 API Docs:     http://localhost:8000/docs"
        echo "📍 Frontend UI:  http://localhost:3000"
        echo "============================================"
        echo ""
        echo "📊 View logs with: docker-compose logs -f"
        echo "🛑 Stop with: docker-compose down"
        echo ""
        
        # Wait for services to be ready
        echo "⏳ Waiting for services to be ready..."
        sleep 10
        
        # Open browser (if available)
        if command_exists xdg-open; then
            xdg-open http://localhost:3000
        elif command_exists open; then
            open http://localhost:3000
        fi
        
        # Show logs
        docker-compose logs -f
        exit 0
    fi
fi

# Local development mode
echo -e "${YELLOW}💻 Starting in local development mode...${NC}"
echo ""

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "next" 2>/dev/null
sleep 2

# Check Python
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed!${NC}"
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed!${NC}"
    exit 1
fi

# Setup Python virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt >/dev/null 2>&1

# Check frontend dependencies
if [ ! -d "frontend-nextjs/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend-nextjs
    npm install
    cd ..
fi

# Export Python path
export PYTHONPATH=$(pwd)

# Start backend
echo "🔧 Starting Backend Server (Port 8000)..."
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
sleep 5

# Start frontend
echo "🎨 Starting Frontend Server (Port 3000)..."
cd frontend-nextjs
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 10

echo ""
echo "============================================"
echo -e "${GREEN}✅ Servers Started Successfully!${NC}"
echo "============================================"
echo "📍 Backend API:  http://127.0.0.1:8000"
echo "📍 API Docs:     http://127.0.0.1:8000/docs"
echo "📍 Frontend UI:  http://localhost:3000"
echo "============================================"
echo ""
echo "📊 Backend PID: $BACKEND_PID (logs: backend.log)"
echo "📊 Frontend PID: $FRONTEND_PID (logs: frontend.log)"
echo ""
echo "🛑 Press Ctrl+C to stop all servers"
echo ""

# Open browser (if available)
sleep 3
if command_exists xdg-open; then
    xdg-open http://localhost:3000
elif command_exists open; then
    open http://localhost:3000
fi

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

# Keep script running
tail -f backend.log frontend.log

