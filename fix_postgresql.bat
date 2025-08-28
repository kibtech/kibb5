@echo off
echo Fixing PostgreSQL installation for Windows...

echo Step 1: Installing packages without psycopg2-binary first...
pip install Flask==2.3.3
pip install Flask-RESTful==0.3.10  
pip install Flask-JWT-Extended==4.5.3
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Migrate==4.0.5
pip install Flask-CORS==4.0.0
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install bcrypt==4.0.1
pip install cryptography==41.0.7
pip install Werkzeug==2.3.7

echo Step 2: Installing Professional Admin Portal Dependencies...
pip install pyotp==2.9.0
pip install qrcode==7.4.2
pip install Pillow==10.0.1
pip install psutil==5.9.6
pip install redis==5.0.1

echo Step 3: Trying to install PostgreSQL adapter with different methods...

echo Method 1: Try installing pre-compiled wheel...
pip install --only-binary=psycopg2-binary psycopg2-binary

if %ERRORLEVEL% NEQ 0 (
    echo Method 1 failed. Trying Method 2: Different version...
    pip install psycopg2-binary==2.9.5
)

if %ERRORLEVEL% NEQ 0 (
    echo Method 2 failed. Trying Method 3: Latest version...
    pip install psycopg2-binary --no-cache-dir
)

if %ERRORLEVEL% NEQ 0 (
    echo All PostgreSQL methods failed. Using alternative psycopg2-binary-compat...
    pip install psycopg2-binary-compat
)

echo Installation complete! Testing the setup...
python -c "import flask_jwt_extended; print('✅ Flask-JWT-Extended installed successfully')"
python -c "import psycopg2; print('✅ PostgreSQL adapter installed successfully')" 2>nul || echo "⚠️  PostgreSQL adapter not installed - you may need to install PostgreSQL"

echo Done! You can now run: python run.py
pause