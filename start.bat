@echo off
REM Quick Start Script for Windows
echo.
echo ========================================
echo AI Cyber Defense - Quick Start (Windows)
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/5] Installing dependencies...
pip install -q -r requirements.txt

echo [3/5] Creating database...
python setup.py

echo.
echo [4/5] Starting Flask server...
echo.
echo ========================================
echo ✓ Setup Complete!
echo ========================================
echo.
echo 🌐 Open browser: http://localhost:5000
echo 🔑 Demo User: admin / password123
echo.
python app.py
