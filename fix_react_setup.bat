@echo off
echo Fixing React setup for KibTech Frontend...

echo Step 1: Installing Create React App dependencies...
npm install react-scripts --save

echo Step 2: Installing React core dependencies...
npm install react react-dom --save

echo Step 3: Installing React Router...
npm install react-router-dom --save

echo Step 4: Installing Admin Portal dependencies...
npm install @heroicons/react recharts axios react-hot-toast --save

echo Step 5: Installing additional dependencies...
npm install web-vitals @testing-library/jest-dom @testing-library/react @testing-library/user-event --save

echo All dependencies installed! You can now run: npm start

pause