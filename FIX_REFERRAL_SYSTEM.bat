@echo off
echo.
echo ========================================
echo    KIBB REFERRAL SYSTEM FIX
echo ========================================
echo.
echo This will fix your referral commission tracking system
echo that's not working when referred users make payments.
echo.
echo Press any key to continue...
pause >nul

echo.
echo Step 1: Checking current referral system status...
python check_referral_system.py

echo.
echo Step 2: Applying fixes to referral system...
python fix_referral_commission_system.py

echo.
echo Step 3: Verifying the fix...
python check_referral_system.py

echo.
echo ========================================
echo    REFERRAL SYSTEM FIX COMPLETED
echo ========================================
echo.
echo Your referral commission system should now work properly!
echo.
echo What was fixed:
echo - Referral relationships between users
echo - Commission settings and rates  
echo - Retroactive commission processing
echo - Commission system verification
echo.
echo Press any key to exit...
pause >nul 