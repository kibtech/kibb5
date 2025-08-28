@echo off
echo ====================================
echo   QUICK BUILD (No Installs)
====================================
echo.

cd /d "%~dp0\frontend"
echo Current directory: %cd%
echo.

echo Trying npm run build...
call npm run build
if %ERRORLEVEL% EQU 0 (
    echo ✅ npm run build worked!
    goto copy
)

echo npm run build failed, trying npx...
call npx react-scripts build
if %ERRORLEVEL% EQU 0 (
    echo ✅ npx react-scripts build worked!
    goto copy
)

echo Both failed - you need to run a full fix
pause
exit /b 1

:copy
echo.
echo Copying to static...
cd ..
xcopy frontend\build\* static\ /E /Y >nul
echo ✅ DONE!
pause