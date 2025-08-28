@echo off
echo 🚀 Setting up KIBTECH ONLINE STORE database...
echo.

echo 📋 Step 1: Creating database tables...
python setup_database.py
if errorlevel 1 (
    echo ❌ Database setup failed!
    pause
    exit /b 1
)

echo.
echo 🌱 Step 2: Adding sample products...
python seed_products.py
if errorlevel 1 (
    echo ❌ Product seeding failed!
    pause
    exit /b 1
)

echo.
echo ✅ KIBTECH ONLINE STORE setup complete!
echo.
echo 🚀 Next steps:
echo    1. Run: start_backend.bat
echo    2. Run: start_frontend.bat
echo    3. Open: https://kibtech.coke
echo.
pause