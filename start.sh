#!/bin/bash

# MI8 Military Intelligence Dashboard - Startup Script

echo "🚀 Starting MI8 Military Intelligence Dashboard..."

# Check if PostgreSQL is running
if ! docker ps | grep -q postgresql; then
    echo "⚠️  PostgreSQL container not running!"
    echo "Please start PostgreSQL first:"
    echo "  docker start postgresql"
    exit 1
fi

# Check if database exists
DB_EXISTS=$(docker exec postgresql psql -U admin -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='mi8'")
if [ "$DB_EXISTS" != "1" ]; then
    echo "📦 Creating mi8 database..."
    docker exec postgresql psql -U admin -d postgres -c "CREATE DATABASE mi8;"
fi

# Start Backend
echo ""
echo "🔧 Starting Backend..."
cd backend

# Activate virtual environment
source venv/bin/activate

# Start backend in background
echo "Backend starting on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Test backend
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend started successfully!"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start Frontend
echo ""
echo "🎨 Starting Frontend..."
cd ../frontend

echo "Frontend starting on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 MI8 Dashboard is running!"
echo ""
echo "📍 URLs:"
echo "  Frontend:    http://localhost:3000"
echo "  Backend:     http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Handle shutdown
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

# Wait for any process to exit
wait
