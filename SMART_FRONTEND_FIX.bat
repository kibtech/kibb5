@echo off
echo ====================================
echo   SMART FRONTEND FIX (Skip if Working)
====================================
echo.

echo Step 1: Going to frontend directory...
cd /d "%~dp0\frontend"
echo Current directory: %cd%
echo.

echo Step 2: Quick test - checking if build works...
call npm run build >nul 2>&1
if %ERRORLEVEL% eq 0 (
    echo ✅ Build already works! Skipping reset...
    goto :copy_files
)

echo Build doesn't work, need to fix...
echo.

echo Step 3: Smart check - is react-scripts the problem?
call npm ls react-scripts >nul 2>&1
if %ERRORLEVEL% eq 0 (
    echo react-scripts is installed, trying npx...
    call npx react-scripts build
    if %ERRORLEVEL% eq 0 (
        echo ✅ npx worked! Build successful!
        goto :copy_files
    )
)

echo react-scripts has issues, doing minimal fix...
echo.

echo Step 4: Installing only react-scripts...
call npm install react-scripts@5.0.1 --save

echo.
echo Step 5: Testing build...
call npm run build
if %ERRORLEVEL% neq 0 (
    echo Still failing, trying npx...
    call npx react-scripts build
)

:copy_files
echo.
echo Step 6: Copying to static directory...
cd ..
if exist "frontend\build" (
    echo Copying build files...
    xcopy frontend\build\* static\ /E /Y >nul
    echo ✅ SUCCESS! Frontend ready!
) else (
    echo ❌ No build directory found!
    pause
    exit /b 1
)

echo.
echo ====================================
echo   DONE! No more waiting!
====================================
pause