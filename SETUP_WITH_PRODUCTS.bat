@echo off
echo ========================================
echo KibTech Store - Complete Setup
echo ========================================
echo.

echo 🚀 Setting up KibTech Store with default products and services...
echo.

echo 📋 Step 1: Setting up local environment...
python setup_local_environment.py
if %errorlevel% neq 0 (
    echo ❌ Environment setup failed!
    pause
    exit /b 1
)

echo.
echo 📦 Step 2: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Dependency installation failed!
    pause
    exit /b 1
)

echo.
echo 🗄️ Step 3: Initializing database...
python init_local_db.py
if %errorlevel% neq 0 (
    echo ❌ Database initialization failed!
    pause
    exit /b 1
)

echo.
echo 🌱 Step 4: Seeding database with default products and services...
python auto_seed_database.py
if %errorlevel% neq 0 (
    echo ❌ Database seeding failed!
    pause
    exit /b 1
)

echo.
echo 🔧 Step 5: Adding product image URL column...
python add_product_image_url_column.py
if %errorlevel% neq 0 (
    echo ❌ Database migration failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Setup completed successfully!
echo ========================================
echo.
echo 📊 What was added:
echo - 4 Product Categories (Laptops, Smartphones, Accessories, Cyber Services)
echo - 9 Tech Products (Laptops, Smartphones, Accessories)
echo - 6 Cyber Services (Security, Recovery, Training, etc.)
echo - 1 Admin User (admin@kibtech.co.ke / admin123)
echo.
echo 🌐 Access your store:
echo - Local: http://localhost:5000
echo - Production: https://kibtech.co.ke
echo.
echo 🔑 Admin Login:
echo - Email: admin@kibtech.co.ke
echo - Password: admin123 (change in production)
echo.
echo 🚀 Starting the application...
echo.
python wsgi.py
pause 