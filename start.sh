#!/bin/bash
# Startup script for Heart Disease Predictor API

echo " Starting Heart Disease Predictor API..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo " Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo " Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo " Installing dependencies..."
pip install -r requirements.txt -q

# Run tests
echo " Running tests..."
pytest tests/ -v

# Start the application
echo " Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
