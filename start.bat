@echo off
echo 🤖 Starting AI-Powered Chatbot System...
echo.

REM Start backend server
echo 🚀 Starting backend server...
start "Backend Server" cmd /k "cd /d \"d:\Actual Personal File\BaterialVagi\Images\chatbot-system\backend\" && C:/Users/Lenovo/AppData/Local/Microsoft/WindowsApps/python3.12.exe main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend server
echo 🌐 Starting frontend server...
start "Frontend Server" cmd /k "cd /d \"d:\Actual Personal File\BaterialVagi\Images\chatbot-system\frontend\" && C:/Users/Lenovo/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m http.server 3000"

REM Wait a moment for frontend to start
timeout /t 3 /nobreak > nul

echo.
echo ✅ System started successfully!
echo.
echo 🔗 Backend API: http://localhost:8000
echo 🔗 API Documentation: http://localhost:8000/docs
echo 🔗 Frontend: http://localhost:3000
echo.
echo ⚠️  Make sure you have set your OpenAI API key in backend\.env
echo.
echo 🛑 To stop the system, close the terminal windows or press Ctrl+C in each
echo.
pause
