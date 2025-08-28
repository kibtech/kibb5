#!/usr/bin/env python3
"""
Local Environment Setup for KibTech Store
This script sets up the local environment with proper domain configuration
and ensures the system can run locally without issues.
"""

import os
import sys
import sqlite3
from pathlib import Path

def create_local_env_file():
    """Create a local .env file with proper configuration"""
    env_content = """# Local Development Environment Configuration
# Database Configuration - Using SQLite for local development
DATABASE_URL=sqlite:///kibtech_local.db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here-local-dev

# Flask Configuration
FLASK_ENV=development
FLASK_CONFIG=local
SECRET_KEY=your-flask-secret-key-local-dev

# M-Pesa Daraja API Configuration - Local Development
MPESA_CONSUMER_KEY=3yOAC0yXFibCzvMQz4hh0ORIDcM1ai947hI1Rt0Fe3yYj5L5
MPESA_CONSUMER_SECRET=ptg1TQDPaKNiIVWhpxMYDk8NAPiFMGiA062Nt7EGGovsNxuZeFTHPXgwgE4umWJf
MPESA_SHORTCODE=3547179
MPESA_PASSKEY=e0232ed3a06890a62b026b48a7c9ba25e1217825a76312907a1c3cfaffb48856
MPESA_INITIATOR_NAME=testapi
MPESA_INITIATOR_PASSWORD=your_initiator_password
# Local callback URLs for development
MPESA_CALLBACK_URL=http://localhost:5000/api/mpesa/callback
MPESA_RESULT_URL=https://kibtech.co.ke/api/mpesa/b2c-result
MPESA_TIMEOUT_URL=https://kibtech.co.ke/api/mpesa/timeout
MPESA_BASE_URL=https://api.safaricom.co.ke

# Environment
ENVIRONMENT=development

# Brevo (formerly Sendinblue) Email Configuration
BREVO_API_KEY=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
BREVO_SMTP_SERVER=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_LOGIN=93a1ce001@smtp-brevo.com
BREVO_SMTP_PASSWORD=pw2VX3bZBEScz4T7

# Email Settings
MAIL_DEFAULT_SENDER=emmkash20@gmail.com
MAIL_DEFAULT_SENDER_NAME=KibTech Store (Local)
MAIL_DEFAULT_REPLY_TO=emmkash20@gmail.com
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file for local development")

def create_local_database():
    """Create local SQLite database"""
    try:
        # Create database file
        db_path = Path('kibtech_local.db')
        if not db_path.exists():
            conn = sqlite3.connect('kibtech_local.db')
            conn.close()
            print("✅ Created local SQLite database: kibtech_local.db")
        else:
            print("✅ Local SQLite database already exists")
        
        return True
    except Exception as e:
        print(f"❌ Error creating local database: {e}")
        return False

def check_domain_configuration():
    """Check and verify domain configuration"""
    print("\n🔍 Checking domain configuration...")
    
    # Check config.py
    with open('config.py', 'r') as f:
        config_content = f.read()
        if 'kibtech.co.ke' in config_content:
            print("✅ config.py has correct domain: kibtech.co.ke")
        else:
            print("❌ config.py has incorrect domain")
    
    # Check config_local.py
    with open('config_local.py', 'r') as f:
        local_config_content = f.read()
        if 'kibtech.co.ke' in local_config_content:
            print("✅ config_local.py has correct domain: kibtech.co.ke")
        else:
            print("❌ config_local.py has incorrect domain")
    
    # Check .envv file
    if os.path.exists('.envv'):
        with open('.envv', 'r') as f:
            envv_content = f.read()
            if 'kibtech.co.ke' in envv_content:
                print("✅ .envv file has correct domain: kibtech.co.ke")
            else:
                print("❌ .envv file has incorrect domain")

def setup_local_app_config():
    """Create a local app configuration that ensures local development works"""
    local_app_config = """#!/usr/bin/env python3
\"\"\"
Local App Configuration for KibTech Store
This ensures the app can run locally with proper configuration
\"\"\"

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_local_config():
    \"\"\"Get local configuration for development\"\"\"
    return {
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'your-flask-secret-key-local-dev'),
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL', 'sqlite:///kibtech_local.db'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', 'your-super-secret-jwt-key-here-local-dev'),
        'JWT_ACCESS_TOKEN_EXPIRES': False,
        'DEBUG': True,
        'ENVIRONMENT': 'development',
        # M-Pesa Configuration for local development
        'MPESA_CONSUMER_KEY': os.environ.get('MPESA_CONSUMER_KEY'),
        'MPESA_CONSUMER_SECRET': os.environ.get('MPESA_CONSUMER_SECRET'),
        'MPESA_SHORTCODE': os.environ.get('MPESA_SHORTCODE'),
        'MPESA_PASSKEY': os.environ.get('MPESA_PASSKEY'),
        'MPESA_INITIATOR_NAME': os.environ.get('MPESA_INITIATOR_NAME'),
        'MPESA_INITIATOR_PASSWORD': os.environ.get('MPESA_INITIATOR_PASSWORD'),
        'MPESA_CALLBACK_URL': os.environ.get('MPESA_CALLBACK_URL', 'http://localhost:5000/api/mpesa/callback'),
        'MPESA_RESULT_URL': os.environ.get('MPESA_RESULT_URL', 'https://kibtech.co.ke/api/mpesa/b2c-result'),
        'MPESA_TIMEOUT_URL': os.environ.get('MPESA_TIMEOUT_URL', 'https://kibtech.co.ke/api/mpesa/timeout'),
        'MPESA_BASE_URL': os.environ.get('MPESA_BASE_URL', 'https://api.safaricom.co.ke'),
        # Email Configuration
        'BREVO_API_KEY': os.environ.get('BREVO_API_KEY'),
        'BREVO_SMTP_SERVER': os.environ.get('BREVO_SMTP_SERVER'),
        'BREVO_SMTP_PORT': int(os.environ.get('BREVO_SMTP_PORT', 587)),
        'BREVO_SMTP_LOGIN': os.environ.get('BREVO_SMTP_LOGIN'),
        'BREVO_SMTP_PASSWORD': os.environ.get('BREVO_SMTP_PASSWORD'),
        'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER'),
        'MAIL_DEFAULT_SENDER_NAME': os.environ.get('MAIL_DEFAULT_SENDER_NAME'),
        'MAIL_DEFAULT_REPLY_TO': os.environ.get('MAIL_DEFAULT_REPLY_TO'),
    }

if __name__ == "__main__":
    config = get_local_config()
    print("Local configuration loaded successfully!")
    print(f"Database URI: {config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Environment: {config['ENVIRONMENT']}")
    print(f"Debug Mode: {config['DEBUG']}")
"""
    
    with open('local_app_config.py', 'w') as f:
        f.write(local_app_config)
    
    print("✅ Created local_app_config.py for local development")

def create_local_startup_script():
    """Create a local startup script"""
    startup_script = """@echo off
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
python app.py
pause
"""
    
    with open('START_LOCAL.bat', 'w') as f:
        f.write(startup_script)
    
    print("✅ Created START_LOCAL.bat for easy local startup")

def main():
    """Main setup function"""
    print("🚀 Setting up KibTech Store for Local Development")
    print("=" * 50)
    
    # Create local environment file
    create_local_env_file()
    
    # Create local database
    create_local_database()
    
    # Check domain configuration
    check_domain_configuration()
    
    # Setup local app configuration
    setup_local_app_config()
    
    # Create local startup script
    create_local_startup_script()
    
    print("\n" + "=" * 50)
    print("✅ Local environment setup completed!")
    print("\n📋 Next Steps:")
    print("1. Run: START_LOCAL.bat (Windows) or python app.py (Linux/Mac)")
    print("2. Access the application at: http://localhost:5000")
    print("3. The system will use kibtech.co.ke for production URLs")
    print("4. Local development uses SQLite database")
    print("\n🔧 Configuration Details:")
    print("- Domain: kibtech.co.ke (correctly configured)")
    print("- Local Database: kibtech_local.db")
    print("- Environment: development")
    print("- Debug Mode: enabled")
    print("\n🌐 Production URLs will point to kibtech.co.ke")
    print("🖥️  Local development will work on localhost:5000")

if __name__ == "__main__":
    main() 