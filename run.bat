@echo off
cleecho ============================================
echo 📊 مُـفـــــوْتِــــر - Smart Invoice Analyzer
echo ============================================
echo.
echo 🚀 Starting Backend (FastAPI) + Frontend (Next.js)...
echo.

REM 🔹 Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b
)

REM 🔹 Activate virtual environment
call venv\Scripts\activate

REM 🔹 Set PYTHONPATH to current directory
set PYTHONPATH=%cd%

REM 🔹 Start FastAPI backend in new window
echo 🔧 Starting Backend Server (Port 8000)...
start "Backend - FastAPI" cmd /k "cd /d %cd% && call venv\Scripts\activate && python -m uvicorn backend.main:app --reload --port 8000"

REM 🔹 Wait 3 seconds for backend to start
timeout /t 3 >nul

REM 🔹 Check if node_modules exists in frontend-nextjs
if not exist "frontend-nextjs\node_modules" (
    echo.
    echo ⚠️  Frontend dependencies not installed!
    echo 📦 Installing dependencies... (this may take a few minutes)
    cd frontend-nextjs
    call npm install
    cd ..
)

REM 🔹 Start Next.js frontend in new window
echo 🎨 Starting Frontend Server (Port 3000)...
start "Frontend - Next.js" cmd /k "cd /d %cd%\frontend-nextjs && npm run dev"

REM 🔹 Wait 5 seconds for frontend to start
timeout /t 5 >nul

echo.
echo ============================================
echo ✅ Servers Started Successfully!
echo ============================================
echo.
echo 📍 Backend API:  http://127.0.0.1:8000
echo 📍 API Docs:     http://127.0.0.1:8000/docs
echo 📍 Frontend UI:  http://localhost:3000
echo.
echo ⚠️  To stop servers: Close both terminal windows
echo ============================================
echo.

pause
