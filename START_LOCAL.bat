@echo off
echo Starting KibTech Store in Local Development Mode...
echo.
echo Domain: kibtech.co.ke (configured for production)
echo Local URL: http://localhost:5000
echo Database: SQLite (kibtech_local.db)
echo.
echo Loading local environment...
set FLASK_CONFIG=local
set FLASK_ENV=development
set ENVIRONMENT=development
echo.
echo Starting Flask application...
python wsgi.py
pause
