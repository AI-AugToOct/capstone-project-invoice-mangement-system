@echo off
chcp 65001 > nul
cls
echo ============================================
echo Smart Invoice Analyzer - Full Stack Starter
echo ============================================
echo.

REM Check if Docker is available
where docker >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Docker detected. Choose startup mode:
    echo 1] Run with Docker (recommended for production-like environment^)
    echo 2] Run locally (development mode^)
    echo.
    choice /C 12 /N /M "Enter choice [1-2]: "
    
    if errorlevel 2 goto LOCAL_MODE
    if errorlevel 1 goto DOCKER_MODE
)

:LOCAL_MODE
echo.
echo Starting in local development mode...
echo.

REM Kill any existing processes
echo Cleaning up old processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment!
        echo Please ensure Python 3.8+ is installed.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install backend dependencies
echo Installing backend dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1

REM Check if node_modules exists in frontend
if not exist "frontend-nextjs\node_modules" (
    echo Installing frontend dependencies...
    cd frontend-nextjs
    call npm install
    cd ..
)

REM Set PYTHONPATH
set PYTHONPATH=%cd%

REM Start FastAPI backend in new window
echo Starting Backend Server (Port 8000^)...
start "Backend - FastAPI" cmd /k "cd /d %cd% && call venv\Scripts\activate && set PYTHONPATH=%cd% && python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"

REM Wait for backend
echo    Waiting for backend to start...
timeout /t 8 /nobreak >nul

REM Start Next.js frontend in new window
echo Starting Frontend Server (Port 3000^)...
start "Frontend - Next.js" cmd /k "cd /d %cd%\frontend-nextjs && npm run dev"

REM Wait for frontend
echo    Waiting for frontend to start...
timeout /t 10 /nobreak >nul

echo.
echo ============================================
echo Servers Started Successfully!
echo ============================================
echo.
echo Backend API:  http://127.0.0.1:8000
echo API Docs:     http://127.0.0.1:8000/docs
echo Frontend UI:  http://localhost:3000
echo.
echo ============================================
echo.
echo If you see 404, wait 10 seconds and press Ctrl+Shift+R
echo To stop servers: Close both terminal windows
echo.

REM Open browser
timeout /t 3 /nobreak >nul
start http://localhost:3000

pause
exit /b 0

:DOCKER_MODE
echo.
echo Starting with Docker...
echo.

REM Stop any existing containers
echo Cleaning up old containers...
docker-compose down >nul 2>&1

REM Build and start containers
echo Building Docker images...
docker-compose build

if %ERRORLEVEL% NEQ 0 (
    echo Failed to build Docker images!
    pause
    exit /b 1
)

echo Starting containers...
docker-compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo Failed to start containers!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Docker containers started successfully!
echo ============================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend UI:  http://localhost:3000
echo ============================================
echo.
echo View logs with: docker-compose logs -f
echo Stop with: docker-compose down
echo.

REM Wait for services
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Open browser
start http://localhost:3000

echo.
echo Press any key to view logs (Ctrl+C to exit^)...
pause >nul
docker-compose logs -f
exit /b 0
