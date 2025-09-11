#!/bin/bash

# AI Chatbot Setup Script
# This script sets up the entire chatbot system

echo "🤖 Setting up AI-Powered Chatbot System..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Setup backend
echo "📦 Setting up backend..."
cd backend

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env exists, if not create from template
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    cp .env .env.example
    echo "📝 Please edit .env file with your OpenAI API key"
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo "DATABASE_URL=sqlite:///./chatbot.db" >> .env
fi

# Initialize database
echo "🗄️  Initializing database..."
python init_db.py

# Start backend server in background
echo "🚀 Starting backend server..."
python main.py &
BACKEND_PID=$!

echo "✅ Backend server started (PID: $BACKEND_PID)"
echo "📊 API available at: http://localhost:8000"
echo "📖 API docs available at: http://localhost:8000/docs"

# Setup frontend
cd ../frontend
echo "🌐 Setting up frontend..."

# Start simple HTTP server
echo "🚀 Starting frontend server..."
python -m http.server 3000 &
FRONTEND_PID=$!

echo "✅ Frontend server started (PID: $FRONTEND_PID)"
echo "🌐 Frontend available at: http://localhost:3000"

echo ""
echo "🎉 Setup complete!"
echo "🔧 Backend API: http://localhost:8000"
echo "🖥️  Frontend: http://localhost:3000"
echo ""
echo "📝 To stop the servers:"
echo "kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "⚠️  Don't forget to add your OpenAI API key to backend/.env"
