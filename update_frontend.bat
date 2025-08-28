@echo off
echo ====================================
echo    KIBTECH Frontend Update Script
echo ====================================
echo.

:: Check if we're in the right directory
if not exist "frontend" (
    echo Error: frontend directory not found!
    echo Make sure you're running this from the KIBTECH FINAL directory
    pause
    exit /b 1
)

if not exist "static" (
    echo Error: static directory not found!
    echo Make sure you're running this from the KIBTECH FINAL directory
    pause
    exit /b 1
)

echo Step 1: Building React frontend...
echo.
cd frontend
call npm run build

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: React build failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Copying build files to Flask static directory...
echo.
cd ..

:: Copy all files from frontend/build to static/
xcopy frontend\build\* static\ /E /Y

if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: Failed to copy files!
    pause
    exit /b 1
)

echo.
echo Step 3: Organizing static files...
echo.

:: Move CSS and JS files to correct locations (if they exist in nested static folder)
if exist "static\static\css" (
    echo Moving CSS files...
    move static\static\css\* static\css\ >nul 2>&1
    rmdir static\static\css >nul 2>&1
)

if exist "static\static\js" (
    echo Moving JS files...
    move static\static\js\* static\js\ >nul 2>&1
    rmdir static\static\js >nul 2>&1
)

:: Remove empty nested static directory if it exists
if exist "static\static" (
    rmdir static\static >nul 2>&1
)

echo.
echo ====================================
echo    ✅ Frontend Update Complete!
echo ====================================
echo.
echo Your React frontend changes are now available in Flask!
echo You can restart your Flask server to see the changes.
echo.
echo To start Flask server: python -m flask run
echo.
pause