#!/bin/bash

# Smart Office - React Django Connection Startup Script
echo "🚀 Starting Smart Office System..."
echo "======================================"

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Django Backend
echo "📡 Starting Django Backend on http://127.0.0.1:8000..."
cd "$SCRIPT_DIR"
python3 manage.py runserver 8000 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# React Frontend
echo "⚡ Starting React Frontend on http://localhost:3000..."
cd "$SCRIPT_DIR/react-frontend"
npm run dev &
REACT_PID=$!

# Wait a moment for React to start
sleep 5

echo "✅ System started successfully!"
echo "=============================="
echo "🎨 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://127.0.0.1:8000"
echo "👨‍💻 Admin:    http://127.0.0.1:8000/admin/"
echo ""
echo "Test Account:"
echo "📧 Email:    test@example.com"
echo "🔑 Password: testpass123"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to kill both processes when script is terminated
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $DJANGO_PID 2>/dev/null
    kill $REACT_PID 2>/dev/null
    echo "✅ Servers stopped."
    exit 0
}

# Set trap to cleanup processes on script termination
trap cleanup SIGINT SIGTERM

# Wait for user to press Ctrl+C
wait
