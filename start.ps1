# Smart Invoice Analyzer - Main Application Launcher
# =================================================
# This PowerShell script starts both the FastAPI backend and Streamlit frontend
# with proper support for Arabic filenames and encoding.
#
# Usage: .\start.ps1
# =================================================

Write-Host "--------------------------------------------" -ForegroundColor Cyan
Write-Host "🚀 Starting Smart Invoice Analyzer" -ForegroundColor Green
Write-Host "--------------------------------------------" -ForegroundColor Cyan

# Activate virtual environment and set PYTHONPATH
$env:PYTHONPATH = Get-Location

# Start FastAPI backend
Write-Host "Starting backend..." -ForegroundColor Yellow
Start-Process -FilePath "C:\Users\HP\capstone-project-invoice-mangement-system\venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "backend.main:app", "--reload", "--port", "8000" -WindowStyle Hidden

# Wait for backend to start
Start-Sleep -Seconds 5

# Start Streamlit frontend with Arabic filename
Write-Host "Starting frontend..." -ForegroundColor Yellow
Set-Location "frontend"
& "C:\Users\HP\capstone-project-invoice-mangement-system\venv\Scripts\python.exe" -m streamlit run "الرئيسية.py"