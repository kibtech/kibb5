@echo off
echo 🔧 Setting up KIBTECH ONLINE STORE Database...
echo.

echo Step 1: Creating database tables...
python setup_database.py

echo.
echo Step 2: Adding products, categories, and brands...
python seed_products.py

echo.
echo ✅ Setup complete! Your store now has:
echo    - 6 Categories (Smartphones, Laptops, Audio, etc.)
echo    - 6 Brands (Apple, Samsung, Sony, etc.)
echo    - 8 Premium Products with images and details
echo.
echo 🚀 Now run: RUN_KIBTECH_STORE.bat
echo.
pause