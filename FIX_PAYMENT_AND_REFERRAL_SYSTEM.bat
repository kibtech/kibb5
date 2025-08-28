@echo off
echo.
echo ========================================
echo    KIBB PAYMENT & REFERRAL SYSTEM FIX
echo ========================================
echo.
echo This will fix TWO critical issues:
echo 1. Cyber service payments not being marked as 'paid'
echo 2. Referral commissions not being tracked
echo.
echo Press any key to continue...
pause >nul

echo.
echo Step 1: Checking current system status...
python check_referral_system.py

echo.
echo Step 2: Applying comprehensive fixes...
python fix_payment_and_referral_system.py

echo.
echo Step 3: Verifying the fix...
python check_referral_system.py

echo.
echo ========================================
echo    SYSTEM FIX COMPLETED
echo ========================================
echo.
echo What was fixed:
echo - Payment status inconsistencies ('completed' -> 'paid')
echo - Referral relationships between users
echo - Commission settings and rates
echo - Retroactive commission processing
echo - MPesa callback system updated
echo.
echo Your system should now:
echo - Properly mark cyber service payments as 'paid'
echo - Track referral commissions correctly
echo - Process all existing missed commissions
echo.
echo Press any key to exit...
pause >nul 