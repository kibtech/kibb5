#!/usr/bin/env python3
"""
Fix Admin Login Issues
This script will ensure admin user exists and login works properly
"""

from app import create_app, db
from app.models import AdminUser, AdminRole
import bcrypt

def fix_admin_login():
    """Fix admin login issues"""
    print("🔧 Fixing Admin Login Issues...")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        try:
            # 1. Ensure admin role exists
            print("1. Checking admin role...")
            admin_role = AdminRole.query.filter_by(name='Super Admin').first()
            if not admin_role:
                print("   Creating Super Admin role...")
                admin_role = AdminRole(
                    name='Super Admin',
                    description='Full system access',
                    permissions=['*']  # All permissions
                )
                db.session.add(admin_role)
                db.session.commit()
                print("   ✅ Super Admin role created!")
            else:
                print("   ✅ Super Admin role already exists!")
            
            # 2. Ensure admin user exists with correct credentials
            print("\n2. Checking admin user...")
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if not admin_user:
                print("   Creating admin user...")
                admin_user = AdminUser(
                    username='admin',
                    email='kibtechc@gmail.com',
                    first_name='KibTech',
                    last_name='Admin',
                    phone='254712591937',
                    role_id=admin_role.id,
                    is_active=True,
                    is_super_admin=True,
                    email_verified=True
                )
                admin_user.set_password('Kibtechceo@2018')
                db.session.add(admin_user)
                db.session.commit()
                print("   ✅ Admin user created successfully!")
            else:
                print("   ✅ Admin user already exists!")
                
                # Ensure user is active and has correct password
                if not admin_user.is_active:
                    print("   Activating admin user...")
                    admin_user.is_active = True
                    db.session.commit()
                    print("   ✅ Admin user activated!")
                
                # Reset password to ensure it's correct
                print("   Resetting password...")
                admin_user.set_password('Kibtechceo@2018')
                admin_user.is_super_admin = True
                admin_user.email_verified = True
                db.session.commit()
                print("   ✅ Password reset successfully!")
            
            # 3. Verify the setup
            print("\n3. Verifying setup...")
            
            # Test password verification
            if admin_user.check_password('Kibtechceo@2018'):
                print("   ✅ Password verification successful!")
            else:
                print("   ❌ Password verification failed!")
                return
            
            # Check user status
            print(f"   ✅ User active: {admin_user.is_active}")
            print(f"   ✅ Super admin: {admin_user.is_super_admin}")
            print(f"   ✅ Email verified: {admin_user.email_verified}")
            print(f"   ✅ Role: {admin_user.role.name if admin_user.role else 'No role'}")
            
            # 4. Display login credentials
            print("\n4. Login Credentials:")
            print("   Email: kibtechc@gmail.com")
            print("   Password: Kibtechceo@2018")
            print("   URL: http://localhost:5000/admin/login")
            
            # 5. Test database connection
            print("\n5. Testing database connection...")
            try:
                result = db.session.execute('SELECT 1')
                print("   ✅ Database connection successful!")
            except Exception as e:
                print(f"   ❌ Database connection failed: {e}")
                return
            
            print("\n✅ Admin login setup completed successfully!")
            print("\nNext steps:")
            print("1. Start your Flask server: python app.py")
            print("2. Navigate to: http://localhost:5000/admin")
            print("3. Login with the credentials above")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

def check_admin_users():
    """List all admin users"""
    print("\n📋 Current Admin Users:")
    print("=" * 30)
    
    app = create_app()
    
    with app.app_context():
        try:
            admin_users = AdminUser.query.all()
            if admin_users:
                for user in admin_users:
                    print(f"Email: {user.email}")
                    print(f"Name: {user.first_name} {user.last_name}")
                    print(f"Active: {user.is_active}")
                    print(f"Super Admin: {user.is_super_admin}")
                    print(f"Role: {user.role.name if user.role else 'No role'}")
                    print("-" * 20)
            else:
                print("No admin users found!")
                
        except Exception as e:
            print(f"Error listing admin users: {e}")

if __name__ == '__main__':
    fix_admin_login()
    check_admin_users() 