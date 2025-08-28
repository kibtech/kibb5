#!/usr/bin/env python3
"""
Fix Admin Password Script
Update the admin user password to the correct one
"""

import os
import sys
from app import create_app, db
from app.models import AdminUser

def fix_admin_password():
    """Fix admin user password"""
    print("🔧 Fixing admin user password...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Find the admin user
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if not admin:
                print("❌ Admin user not found")
                return False
            
            print(f"✅ Found admin user: {admin.first_name} {admin.last_name}")
            print(f"   Email: {admin.email}")
            print(f"   Current active status: {admin.is_active}")
            
            # Update password to the correct one
            new_password = 'Kibtechceo@2018'
            admin.set_password(new_password)
            
            # Ensure user is active
            admin.is_active = True
            
            db.session.commit()
            
            print("✅ Admin password updated successfully!")
            print(f"   New password: {new_password}")
            print(f"   Active status: {admin.is_active}")
            
            # Test the new password
            if admin.check_password(new_password):
                print("✅ Password verification successful!")
                return True
            else:
                print("❌ Password verification failed after update")
                return False
                
        except Exception as e:
            print(f"❌ Error updating admin password: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

def test_admin_login():
    """Test admin login with new password"""
    print("\n🔐 Testing admin login with new password...")
    
    app = create_app()
    
    with app.app_context():
        try:
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if not admin:
                print("❌ Admin user not found")
                return False
            
            # Test password
            if admin.check_password('Kibtechceo@2018'):
                print("✅ Admin login credentials work correctly!")
                print(f"   Email: {admin.email}")
                print(f"   Password: Kibtechceo@2018")
                print(f"   Role: {admin.role.name if admin.role else 'N/A'}")
                print(f"   Active: {admin.is_active}")
                return True
            else:
                print("❌ Admin password verification failed")
                return False
                
        except Exception as e:
            print(f"❌ Error testing admin login: {str(e)}")
            return False

def main():
    """Main function"""
    print("🔧 KIBTECH Admin Password Fix Tool")
    print("=" * 50)
    
    # Fix admin password
    success = fix_admin_password()
    
    if success:
        # Test admin login
        test_admin_login()
        
        print("\n" + "=" * 50)
        print("🎉 Admin password fix completed successfully!")
        print("\n💡 Updated Admin Information:")
        print("📧 Email: kibtechc@gmail.com")
        print("🔑 Password: Kibtechceo@2018")
        print("👤 Role: Super Admin")
        print("🏢 Name: KibTech CEO")
        print("\n🌐 Access admin panel at: https://kibtech.coke/admin")
    else:
        print("\n❌ Failed to fix admin password")
        print("Please check the error messages above")

if __name__ == '__main__':
    main() 