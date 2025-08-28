@echo off
echo ========================================
echo 🔧 KIBTECH DATABASE SCHEMA FIX
echo ========================================

echo Step 1: Fixing database schema...
python fix_database_schema.py

echo.
echo Step 2: Setting up database with products...
python setup_database.py

echo.
echo Step 3: Setting up admin portal...
python setup_admin.py

echo.
echo ✅ Database fix completed!
echo 🎯 Ready to start the application!

pause