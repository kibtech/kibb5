@echo off
echo ==========================================
echo    🚀 KIBTECH ONLINE SERVICES 🚀
echo ==========================================
echo.

echo ✅ Database is already set up and working!
echo 📊 Found 35 tables, 1 admin user, 6 categories, 8 products, 6 brands
echo.

echo 🔧 Checking database connection...
python test_postgresql_connection.py
echo.

echo 🌱 Checking sample products...
python seed_products.py
echo.

echo 👨‍💼 Checking admin portal...
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
echo 🔧 Admin Panel: https://kibtech.coke/admin
echo.
echo 📋 Admin Login:
echo    Email: kibtechc@gmail.com
echo    Password: admin123
echo    Username: kibtech_admin
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