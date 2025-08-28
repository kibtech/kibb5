@echo off
echo ====================================
echo   SIMPLE BUILD
====================================

cd frontend
echo Trying npx react-scripts build...
npx react-scripts build

if exist "build" (
    echo Build successful! Copying files...
    cd ..
    xcopy frontend\build\* static\ /E /Y
    echo DONE!
) else (
    echo Build failed!
)

pause