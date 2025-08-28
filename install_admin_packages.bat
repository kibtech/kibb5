@echo off
echo Installing missing packages for Professional Admin Portal...

cd /d "%~dp0"

echo Installing Heroicons for icons...
npm install @heroicons/react

echo Installing Recharts for charts...
npm install recharts

echo Installing additional dependencies...
npm install axios
npm install react-hot-toast

echo All packages installed successfully!
echo You can now start the frontend with: npm start

pause