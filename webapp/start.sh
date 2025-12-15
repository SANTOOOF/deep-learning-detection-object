#!/bin/bash
# ============================================================================
# Industrial Object Detection - Quick Start Script (Linux/Mac)
# ============================================================================

echo ""
echo "========================================================================"
echo "  INDUSTRIAL OBJECT DETECTION - QUICK START"
echo "========================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
    echo "      Virtual environment created!"
else
    echo "[1/4] Virtual environment already exists."
fi

echo ""
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[3/4] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[4/4] Starting Flask application..."
echo ""
echo "========================================================================"
echo "  APPLICATION STARTING"
echo "========================================================================"
echo ""
echo "  Access the application at: http://127.0.0.1:5000"
echo ""
echo "  Press CTRL+C to stop the server"
echo ""
echo "========================================================================"
echo ""

python app.py
