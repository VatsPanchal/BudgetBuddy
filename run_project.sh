#!/bin/bash

echo "Starting Budget Buddy Setup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 14 or higher from https://nodejs.org/"
    exit 1
fi

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Run database migrations
echo "Setting up database..."
alembic upgrade head

# Start backend server in background
echo "Starting backend server..."
cd backend
source ../venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Install frontend dependencies and start frontend server
echo "Setting up frontend..."
cd ../frontend
npm install
echo "Starting frontend server..."
npm run serve &
FRONTEND_PID=$!

echo "Setup complete! The application will be available at http://localhost:8080"
echo "Press Ctrl+C to stop the servers"

# Wait for user to press Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 