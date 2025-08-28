@echo off
echo.
echo ========================================
echo    FINAL REFERRAL SYSTEM VERIFICATION
echo ========================================
echo.
echo This will run the final verification to ensure
echo all referral relationships are properly established.
echo.
echo Press any key to continue...
pause >nul

echo.
echo Step 1: Fixing remaining referral relationships...
python fix_remaining_referral_relationships.py

echo.
echo Step 2: Final system verification...
python check_referral_system.py

echo.
echo ========================================
echo    VERIFICATION COMPLETED
echo ========================================
echo.
echo If all issues are resolved, your referral system
echo should now work perfectly for all future payments!
echo.
echo Press any key to exit...
pause >nul 