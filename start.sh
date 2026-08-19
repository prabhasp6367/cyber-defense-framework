#!/bin/bash
# Quick Start Script - AI Cyber Defense Framework

echo "\n========================================"
echo "AI Cyber Defense - Quick Start"
echo "========================================\n"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

echo "[2/5] Installing dependencies (this may take 1-2 min)..."
pip install -q -r requirements.txt

echo "[3/5] Creating database..."
python3 setup.py

echo "\n[4/5] Starting Flask server..."
python3 app.py &

echo "\n========================================"
echo "✓ Setup Complete!"
echo "========================================"
echo ""
echo "🌐 Open browser: http://localhost:5000"
echo "🔑 Demo User: admin / password123"
echo ""
echo "Press Ctrl+C to stop server"
echo ""
