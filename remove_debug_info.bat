@echo off
echo 🔍 Removing Debug Information from Codebase...
echo.

echo 📁 Checking if Node.js is available...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js found
echo.

echo 🚀 Running debug removal script...
node remove_debug_info.js

echo.
echo ✅ Debug removal completed!
echo.
echo 📝 Next steps:
echo 1. Check if debug information is still visible in the UI
echo 2. Test the application functionality
echo 3. If issues persist, check the console for errors
echo.
pause 