@echo off
echo ========================================
echo    KIBTECH CYBER SERVICES SETUP
echo ========================================
echo.

echo [1/4] Creating database migrations...
python -c "
from app import create_app, db
from app.models import CyberService, CyberServiceOrder, CyberServiceForm
app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"

echo.
echo [2/4] Seeding cyber services...
python seed_cyber_services.py

echo.
echo [3/4] Verifying setup...
python -c "
from app import create_app, db
from app.models import CyberService
app = create_app()
with app.app_context():
    count = CyberService.query.count()
    print(f'Found {count} cyber services in database')
    if count > 0:
        print('✅ Cyber services setup completed successfully!')
    else:
        print('❌ No services found. Setup may have failed.')
"

echo.
echo [4/4] Setup complete!
echo.
echo Next steps:
echo 1. Start your backend server: python run.py
echo 2. Start your frontend: cd frontend && npm start
echo 3. Visit https://kibtech.coke/cyber-services
echo.
pause 