@echo off
echo ==========================================
echo    🚀 KIBTECH ONLINE SERVICES 🚀
echo ==========================================
echo.

echo 🔧 Setting up database and products...
python setup_database.py
echo.
echo 🌱 Adding sample products...
python seed_products.py
echo.
echo 👨‍💼 Setting up admin portal...
python setup_admin.py
echo.

echo 🔧 Installing frontend dependencies...
cd frontend
echo Installing React dependencies...
call npm install
echo Installing Admin Portal dependencies...
call npm install @heroicons/react recharts axios react-hot-toast
cd ..
echo.

echo 🚀 Starting KIBTECH ONLINE SERVICES...
echo.
echo 📡 Backend API: http://127.0.0.1:5000
echo 🌐 Frontend Website: https://kibtech.coke
echo.
echo ⚠️  Keep both windows open while testing!
echo.

REM Start backend in new window
start "KIBTECH Backend" cmd /k "python run.py"

REM Wait a moment for backend to start
timeout /t 5 /nobreak > nul

REM Start frontend in new window
start "KIBTECH Frontend" cmd /k "cd frontend && npm start"

echo ✅ KIBTECH ONLINE SERVICES is starting...
echo 🌐 Your website will open automatically in a few seconds!
echo.
echo Press any key to close this window...
pause > nul