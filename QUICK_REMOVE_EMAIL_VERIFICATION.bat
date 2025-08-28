@echo off
echo ============================================================
echo QUICK EMAIL VERIFICATION REMOVAL
echo ============================================================
echo.
echo This will remove email verification requirements from:
echo - User registration
echo - Password reset
echo - Login process
echo.
echo Starting process...
echo.

python remove_email_verification_complete.py

echo.
echo ============================================================
echo PROCESS COMPLETED!
echo ============================================================
echo.
echo Next steps:
echo 1. Run the SQL commands in migrate_email_verification.sql
echo 2. Restart your Flask application
echo 3. Test user registration and password reset
echo.
pause 