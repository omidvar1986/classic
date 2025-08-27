#!/bin/bash

# Start Django backend
echo "Starting Django backend..."
cd /Users/miladomidvar/Desktop/Djangoproject/calssic_sys
python3 manage.py runserver 127.0.0.1:8000 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Start React frontend
echo "Starting React frontend..."
cd react-frontend
npm run dev &
REACT_PID=$!

echo "Both servers are starting..."
echo "Django backend: http://127.0.0.1:8000"
echo "React frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo "Stopping servers..."
    kill $DJANGO_PID $REACT_PID 2>/dev/null
    exit
}

# Set up trap to cleanup on Ctrl+C
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $DJANGO_PID $REACT_PID
