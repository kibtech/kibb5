@echo off
echo Installing Python packages for KibTech Admin Portal...

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

echo Installing Professional Admin Portal Dependencies...
pip install pyotp==2.9.0
pip install qrcode==7.4.2
pip install Pillow==10.0.1
pip install psutil==5.9.6

echo All packages installed successfully!
echo Now you can run: python run.py

pause