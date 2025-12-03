# Speech to Text - Start Script
# This script starts the FastAPI server with the correct Python environment

Write-Host "🎤 Starting Speech to Text Application..." -ForegroundColor Cyan
Write-Host ""

# Set execution policy for this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Navigate to project root
Set-Location "d:\New folder\Speech to text project"

# Start the server using the venv Python
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "Open http://localhost:8000 in your browser" -ForegroundColor Magenta
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

& ".\.venv\Scripts\python.exe" app\main.py
