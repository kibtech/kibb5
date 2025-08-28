@echo off
echo ==========================================
echo    🚀 KIBTECH ONLINE SERVICES 🚀
echo ==========================================
echo.

echo ✅ Starting KibTech application...
echo.
echo 📡 Backend API: https://kibtech.coke:5000
echo 🌐 Frontend Website: https://kibtech.coke
echo 🔧 Admin Panel: https://kibtech.coke/admin
echo.
echo 📋 Admin Login:
echo    Email: kibtechc@gmail.com
echo    Password: admin123
echo    Username: kibtech_admin
echo.

REM Start backend in new window
start "KIBTECH Backend" cmd /k "python run.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend in new window
start "KIBTECH Frontend" cmd /k "cd frontend && npm start"

echo ✅ KIBTECH
 ONLINE SERVICES is starting...
echo 🌐 Your website will open automatically in a few seconds!
echo.
pause 