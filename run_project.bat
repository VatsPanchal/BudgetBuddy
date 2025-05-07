@echo off
echo Starting Budget Buddy Setup...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js 14 or higher from https://nodejs.org/
    pause
    exit /b
)

REM Create and activate virtual environment
echo Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate

REM Install backend dependencies
echo Installing backend dependencies...
cd backend
pip install -r requirements.txt

REM Run database migrations
echo Setting up database...
alembic upgrade head

REM Start backend server in a new window
echo Starting backend server...
start cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000"

REM Install frontend dependencies and start frontend server
echo Setting up frontend...
cd ..\frontend
npm install
echo Starting frontend server...
start cmd /k "cd frontend && npm run serve"

echo Setup complete! The application will be available at http://localhost:8080
echo Press any key to exit this window...
pause >nul 