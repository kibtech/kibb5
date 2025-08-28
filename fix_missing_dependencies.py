#!/usr/bin/env python3
"""
Script to fix missing dependencies issue
This script ensures all required packages are properly listed in requirements.txt
"""

import os
import sys

def check_requirements():
    """Check if all required packages are in requirements.txt"""
    required_packages = [
        'Flask==2.3.3',
        'Flask-SQLAlchemy==3.0.5',
        'Flask-Migrate==4.0.5',
        'Flask-CORS==4.0.0',
        'Flask-JWT-Extended==4.5.3',
        'psycopg2-binary==2.9.7',
        'python-dotenv==1.0.0',
        'bcrypt==4.0.1',
        'Pillow==10.0.1',
        'requests==2.31.0',
        'gunicorn==21.2.0',
        'whitenoise==6.5.0',
        'sib_api_v3_sdk==7.5.0',
        'cryptography==41.0.7'
    ]
    
    print("Checking requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            current_requirements = f.read()
        
        missing_packages = []
        for package in required_packages:
            package_name = package.split('==')[0]
            if package_name not in current_requirements:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"Missing packages: {missing_packages}")
            return False
        else:
            print("All required packages are present in requirements.txt")
            return True
            
    except FileNotFoundError:
        print("requirements.txt not found!")
        return False

def main():
    print("=== KibTech Dependency Check ===")
    print()
    
    if check_requirements():
        print("✅ All dependencies are properly configured")
        print()
        print("Next steps:")
        print("1. Commit the updated requirements.txt")
        print("2. Push to your deployment platform (Heroku, Scalingo, etc.)")
        print("3. The platform should automatically install the missing cryptography package")
        print()
        print("If you're deploying manually:")
        print("   pip install -r requirements.txt")
    else:
        print("❌ Some dependencies are missing")
        print("Please ensure requirements.txt contains all required packages")

if __name__ == "__main__":
    main() 