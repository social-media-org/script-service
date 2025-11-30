#!/bin/bash

# Script Generation Service - Startup Script
# Usage: ./start.sh [port]

set -e

echo "================================"
echo "Script Generation Service"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
    echo "   - DEEPSEEK_API_KEY"
    echo "   - ASSEMBLYAI_API_KEY"
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit..."
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python version: $PYTHON_VERSION"

# Check if dependencies are installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Get port from argument or use default
PORT=${1:-8000}

echo ""
echo "================================"
echo "Starting service on port $PORT"
echo "================================"
echo ""
echo "📖 Documentation:"
echo "   - Swagger UI: http://localhost:$PORT/docs"
echo "   - ReDoc: http://localhost:$PORT/redoc"
echo ""
echo "🔥 Press Ctrl+C to stop"
echo ""

# Start the service
uvicorn app.main:app --reload --host 0.0.0.0 --port $PORT
