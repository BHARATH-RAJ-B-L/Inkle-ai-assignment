@echo off
echo ========================================
echo TripMind AI - Multi-Agent Tourism System
echo ========================================
echo.

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Starting FastAPI backend server...
echo Server will be available at: http://localhost:8000
echo API Docs will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python main.py
