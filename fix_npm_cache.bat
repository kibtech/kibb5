@echo off
echo Fixing NPM cache issues...

echo Step 1: Cleaning NPM cache...
npm cache clean --force

echo Step 2: Removing corrupted files...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

echo Step 3: Fresh installation...
npm install --no-cache

echo Step 4: Installing admin dependencies...
npm install @heroicons/react recharts axios react-hot-toast --no-cache

echo Done! Try: npm start

pause