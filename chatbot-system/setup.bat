@echo off
REM AI Chatbot Setup Script for Windows
REM This script sets up the entire chatbot system

echo 🤖 Setting up AI-Powered Chatbot System...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Setup backend
echo 📦 Setting up backend...
cd backend

REM Install requirements
echo Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env exists, if not create from template
if not exist .env (
    echo ⚠️  .env file not found. Creating template...
    echo OPENAI_API_KEY=your_openai_api_key_here > .env
    echo DATABASE_URL=sqlite:///./chatbot.db >> .env
    echo 📝 Please edit .env file with your OpenAI API key
)

REM Initialize database
echo 🗄️  Initializing database...
python init_db.py

echo 🚀 Backend setup complete!
echo 📊 To start the backend: python main.py
echo 📖 API docs will be available at: http://localhost:8000/docs

cd ..\frontend
echo 🌐 Frontend setup complete!
echo 🚀 To start the frontend: python -m http.server 3000
echo 🖥️  Frontend will be available at: http://localhost:3000

cd ..
echo.
echo 🎉 Setup complete!
echo.
echo 🚀 To start the system:
echo   1. Start backend: cd backend && python main.py
echo   2. Start frontend: cd frontend && python -m http.server 3000
echo.
echo ⚠️  Don't forget to add your OpenAI API key to backend\.env
echo.
pause
