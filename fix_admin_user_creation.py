#!/usr/bin/env python3
"""
Fix Admin User Creation Script
Resolves the 'AdminUser' object has no attribute 'name' error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, AdminUser
from werkzeug.security import generate_password_hash

def fix_admin_creation():
    """Fix admin user creation by checking actual model structure"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Fixing Admin User Creation...")
            
            # Check if admin already exists
            existing_admin = AdminUser.query.first()
            if existing_admin:
                print("✅ Admin user already exists")
                
                # Check what attributes are available
                print("📋 Available admin attributes:")
                for attr in dir(existing_admin):
                    if not attr.startswith('_'):
                        try:
                            value = getattr(existing_admin, attr)
                            if not callable(value):
                                print(f"   {attr}: {value}")
                        except:
                            pass
                return True
            
            # Create new admin user
            print("👤 Creating new admin user...")
            
            # Check AdminUser model structure
            admin_attrs = [attr for attr in dir(AdminUser) if not attr.startswith('_')]
            print(f"📋 AdminUser model attributes: {admin_attrs}")
            
            # Create admin with basic attributes
            admin_data = {
                'username': 'admin',
                'email': 'admin@kibtech.coke',
                'password_hash': generate_password_hash('admin123'),
                'is_admin': True,
                'is_active': True
            }
            
            # Add name if the attribute exists
            if hasattr(AdminUser, 'name'):
                admin_data['name'] = 'System Administrator'
            
            # Add first_name and last_name if they exist
            if hasattr(AdminUser, 'first_name'):
                admin_data['first_name'] = 'System'
            if hasattr(AdminUser, 'last_name'):
                admin_data['last_name'] = 'Administrator'
            
            # Create the admin user
            admin = AdminUser(**admin_data)
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🚀 Admin User Creation Fix")
    print("=" * 40)
    
    success = fix_admin_creation()
    
    if success:
        print("\n✅ Admin user creation fixed successfully!")
    else:
        print("\n❌ Failed to fix admin user creation") 