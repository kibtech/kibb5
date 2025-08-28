@echo off
echo ====================================
echo   NUCLEAR FRONTEND FIX (Complete Reset)
====================================
echo.

echo Step 1: Going to frontend directory...
cd /d "%~dp0\frontend"
echo Current directory: %cd%
echo.

echo Step 2: Nuclear option - deleting node_modules and package-lock.json...
if exist "node_modules" (
    echo Deleting node_modules...
    rmdir /S /Q "node_modules"
)

if exist "package-lock.json" (
    echo Deleting package-lock.json...
    del "package-lock.json"
)

echo.
echo Step 3: Clearing npm cache...
call npm cache clean --force

echo.
echo Step 4: Fresh install of everything...
call npm install

echo.
echo Step 5: Installing react-scripts specifically...
call npm install react-scripts@5.0.1

echo.
echo Step 6: Verifying installation...
call npm ls react-scripts

echo.
echo Step 7: Building frontend...
call npm run build

if %ERRORLEVEL% neq 0 (
    echo Build still failed! Trying npx...
    call npx react-scripts build
)

echo.
echo Step 8: Copying to static directory...
cd ..
if exist "frontend\build" (
    xcopy frontend\build\* static\ /E /Y
    echo ✅ SUCCESS! Frontend built and copied!
) else (
    echo ❌ Build directory not found!
)

echo.
echo ====================================
echo   NUCLEAR FIX COMPLETE!
====================================
pause