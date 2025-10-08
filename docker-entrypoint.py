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

# Debug: Check DATABASE_URL (masked for security)
db_url = os.environ.get('DATABASE_URL', 'NOT SET')
if db_url != 'NOT SET':
    # Show only host part for debugging
    if '@' in db_url:
        host_part = db_url.split('@')[1].split('/')[0] if '/' in db_url.split('@')[1] else db_url.split('@')[1]
        print(f"DEBUG: DATABASE_URL host: {host_part}")
    else:
        print(f"DEBUG: DATABASE_URL: INVALID FORMAT")
else:
    print(f"DEBUG: DATABASE_URL: NOT SET")
print()

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

