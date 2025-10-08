@echo off
chcp 65001 >nul
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║           مُـفـــــوْتِــــر - Smart Invoice Analyzer        ║
echo ║                                                              ║
echo ║        Built with: FastAPI + Next.js + Groq + Supabase      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo.
echo 🚀 Starting Backend + Frontend...
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo ❌ Virtual environment not found!
    echo.
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo.
    echo 📥 Installing dependencies...
    call venv\Scripts\activate
    pip install -r requirements.txt
)

REM Activate virtual environment
call venv\Scripts\activate

REM Set PYTHONPATH
set PYTHONPATH=%cd%

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🔧 Starting Backend (FastAPI on Port 8000)                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
start "مُفوتر Backend - FastAPI" cmd /k "cd /d %cd% && call venv\Scripts\activate && echo ✅ Backend is starting... && python -m uvicorn backend.main:app --reload --port 8000"

REM Wait for backend to start
echo ⏳ Waiting for backend to initialize...
timeout /t 5 >nul

REM Check if frontend dependencies are installed
if not exist "frontend-nextjs\node_modules" (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║  📦 Installing Frontend Dependencies...                      ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    cd frontend-nextjs
    call npm install
    cd ..
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎨 Starting Frontend (Next.js on Port 3000)                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
start "مُفوتر Frontend - Next.js" cmd /k "cd /d %cd%\frontend-nextjs && echo ✅ Frontend is starting... && npm run dev"

REM Wait for frontend to start
echo ⏳ Waiting for frontend to initialize...
timeout /t 8 >nul

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║           ✅ مُـفـــــوْتِــــر Started Successfully!         ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo.
echo 📍 Backend API:     http://127.0.0.1:8000
echo 📍 API Docs:        http://127.0.0.1:8000/docs
echo 📍 Frontend UI:     http://localhost:3000
echo.
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  🎯 Quick Start Guide                                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo  1. Open your browser: http://localhost:3000
echo  2. Click "رفع فاتورة" to upload an invoice
echo  3. Use "الدردشة" to ask questions in Arabic
echo  4. Check "لوحة التحكم" for analytics
echo.
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  💬 Example Questions (Chat)                                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo  • كم أنفقت على المطاعم؟
echo  • أرني فواتير ستاربكس
echo  • ما هو متوسط الفاتورة؟
echo  • كم عدد الفواتير هذا الشهر؟
echo.
echo.
echo ⚠️  To stop servers: Close both terminal windows
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause

