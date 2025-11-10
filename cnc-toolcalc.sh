#!/bin/bash
#################################################################
# CNC-ToolCalc Start Script
# Startet Backend (Port 8000) + Frontend (Port 5173)
#################################################################

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

echo "🚀 Starting CNC-ToolCalc v$(cat VERSION.txt)..."

# Backend starten
echo "📦 Starting Backend (Port 8000)..."
cd 03-development/backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt 2>/dev/null || echo "⚠️  Install requirements first"
uvicorn api.main:app --reload --port 8000 &
BACKEND_PID=$!
cd "$PROJECT_ROOT"

# Frontend starten
echo "🎨 Starting Frontend (Port 5173)..."
cd 03-development/frontend
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi
npm run dev &
FRONTEND_PID=$!
cd "$PROJECT_ROOT"

echo ""
echo "✅ CNC-ToolCalc is running!"
echo ""
echo "Frontend:  http://localhost:5173"
echo "Backend:   http://localhost:8000"
echo "API Docs:  http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop..."

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

wait
