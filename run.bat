@echo off
echo --------------------------------------------
echo 📦 Starting Smart Invoice Analyzer
echo --------------------------------------------

REM 🔹 Activate virtual environment
call venv\Scripts\activate

REM 🔹 Set PYTHONPATH to current directory (fix import issue)
set PYTHONPATH=%cd%

REM 🔹 Start FastAPI backend from root (now fixed for all systems)
start cmd /k "python -m uvicorn backend.main:app --reload --port 8000"

REM 🔹 Wait 5 seconds to let backend start
timeout /t 5 >nul

REM 🔹 Start Streamlit frontend
cd frontend
streamlit run app.py

pause
