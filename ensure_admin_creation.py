#!/usr/bin/env python3
"""
Ensure Admin Creation Script for KIBTECH ONLINE SERVICES
This script ensures admin login details are automatically created
Run with: python ensure_admin_creation.py
"""

import os
import sys
from app import create_app, db
from app.models import AdminUser

def create_default_admin():
    """Create default admin user if not exists"""
    print("👤 Ensuring default admin user exists...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if admin exists
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if admin:
                print("✅ Default admin user already exists:")
                print(f"   Name: {admin.first_name} {admin.last_name}")
                print(f"   Email: {admin.email}")
                print(f"   Role: {admin.role.name if admin.role else 'N/A'}")
                print(f"   Active: {admin.is_active}")
                return admin
            else:
                print("📝 Creating default admin user...")
                
                # Create admin user
                admin = AdminUser(
                    username='kibtech_admin',
                    email='kibtechc@gmail.com',
                    first_name='KC',
                    last_name='KibTech CEO',
                    role_id=1,  # Assuming super admin role has ID 1
                    is_active=True,
                    is_super_admin=True
                )
                admin.set_password('admin123')
                
                db.session.add(admin)
                db.session.commit()
                
                print("✅ Default admin user created successfully!")
                print(f"   Name: {admin.first_name} {admin.last_name}")
                print(f"   Email: {admin.email}")
                print(f"   Password: admin123")
                print(f"   Role: {admin.role.name if admin.role else 'N/A'}")
                print(f"   Active: {admin.is_active}")
                
                return admin
                
        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return None

def test_admin_login():
    """Test admin login functionality"""
    print("\n🔐 Testing admin login credentials...")
    
    app = create_app()
    
    with app.app_context():
        try:
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if not admin:
                print("❌ Admin user not found")
                return False
            
            # Test password
            if admin.check_password('admin123'):
                print("✅ Admin login credentials work correctly!")
                print(f"   Email: {admin.email}")
                print(f"   Password: admin123")
                print(f"   Role: {admin.role}")
                return True
            else:
                print("❌ Admin password verification failed")
                return False
                
        except Exception as e:
            print(f"❌ Error testing admin login: {str(e)}")
            return False

def display_admin_info():
    """Display admin information"""
    print("\n📋 Admin Information:")
    print("=" * 40)
    print("🌐 Admin Panel URL: https://kibtech.coke/admin")
    print("📧 Email: kibtechc@gmail.com")
    print("🔑 Password: admin123")
    print("👤 Role: Super Admin")
    print("🏢 Name: KC KibTech CEO")
    print("=" * 40)

def main():
    """Main function to ensure admin creation"""
    print("🚀 KIBTECH Admin Creation Tool")
    print("=" * 50)
    
    # Create admin if missing
    admin = create_default_admin()
    
    if admin:
        # Test admin login
        test_admin_login()
        
        # Display admin info
        display_admin_info()
        
        print("\n" + "=" * 50)
        print("🎉 Admin setup completed successfully!")
        print("\n💡 Next steps:")
        print("1. Run 'python run.py' to start the backend server")
        print("2. Run 'npm start' in frontend directory")
        print("3. Access admin panel at https://kibtech.coke/admin")
        print("4. Login with the credentials above")
    else:
        print("\n❌ Failed to create admin user")
        print("Please check the error messages above")

if __name__ == '__main__':
    main() 