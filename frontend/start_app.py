"""
Smart Invoice Analyzer - Application Launcher
===========================================
This launcher handles Arabic filenames properly on Windows systems
where batch files may have encoding issues with Arabic characters.

Usage: python start_app.py
"""
import subprocess
import os
import sys

# Change to the frontend directory
os.chdir(r"C:\Users\HP\capstone-project-invoice-mangement-system\frontend")

# Set the Python path
python_exe = r"C:\Users\HP\capstone-project-invoice-mangement-system\venv\Scripts\python.exe"

# Arabic filename for the main application
arabic_filename = "الرئيسية.py"

print("🚀 Starting Smart Invoice Analyzer...")
print(f"📄 Running: {arabic_filename}")
print("🌐 App will be available at: http://localhost:8501")
print("-" * 50)

# Run Streamlit with the Arabic filename
try:
    subprocess.run([python_exe, "-m", "streamlit", "run", arabic_filename], check=True)
except Exception as e:
    print(f"Error: {e}")
    print("Trying alternative approach...")
    
    # Alternative: Copy to temp English name and run
    import shutil
    temp_file = "temp_main.py"
    shutil.copy(arabic_filename, temp_file)
    subprocess.run([python_exe, "-m", "streamlit", "run", temp_file], check=True)