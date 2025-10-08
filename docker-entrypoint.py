#!/usr/bin/env python3
"""
Docker entrypoint script for Railway deployment
Python-based for better cross-platform compatibility
"""
import os
import sys
import subprocess

# Get PORT from environment
port = os.environ.get('PORT', '8000')

print("=" * 50)
print("🚀 Docker Entrypoint (Python)")
print("=" * 50)
print(f"DEBUG: PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
print(f"DEBUG: Using port: {port}")

# Validate port is numeric
try:
    port_int = int(port)
    print(f"✅ Port validation: {port_int} is valid")
except ValueError:
    print(f"❌ ERROR: PORT '{port}' is not a valid integer!")
    sys.exit(1)

# Build command
cmd = [
    "uvicorn",
    "backend.main:app",
    "--host", "0.0.0.0",
    "--port", str(port_int)
]

print(f"DEBUG: Command: {' '.join(cmd)}")
print("=" * 50)
print()

# Execute uvicorn
try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ ERROR: uvicorn failed with code {e.returncode}")
    sys.exit(e.returncode)
except FileNotFoundError:
    print("❌ ERROR: uvicorn not found!")
    sys.exit(1)

