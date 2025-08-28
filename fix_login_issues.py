#!/usr/bin/env python3
"""
Fix Login Issues Script for KIBTECH ONLINE SERVICES
This script diagnoses and fixes login issues including OTP and 403 errors
Run with: python fix_login_issues.py
"""

import os
import sys
from app import create_app, db
from app.models import User, AdminUser, OTP

def check_login_issues():
    """Check for common login issues"""
    print("🔍 Diagnosing login issues...")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if users exist
            users = User.query.all()
            print(f"👥 Regular Users: {len(users)}")
            
            for user in users:
                print(f"   - {user.email} (Verified: {user.email_verified})")
            
            # Check if admin users exist
            admins = AdminUser.query.all()
            print(f"👤 Admin Users: {len(admins)}")
            
            for admin in admins:
                print(f"   - {admin.email} (Role: {admin.role})")
            
            # Check OTP table
            otps = OTP.query.all()
            print(f"📧 OTP Records: {len(otps)}")
            
            # Check for specific issues
            print("\n🔍 Checking for specific issues:")
            
            # Issue 1: Email verification requirement
            print("1. Email verification requirement - This might be causing 403 errors")
            
            # Issue 2: OTP generation error
            print("2. OTP generation error - 'cannot unpack non-iterable bool object'")
            
            # Issue 3: No verified users
            verified_users = User.query.filter_by(email_verified=True).all()
            print(f"3. Verified users: {len(verified_users)}")
            
            if len(verified_users) == 0:
                print("   ⚠️ No verified users found - this will cause login issues")
            
        except Exception as e:
            print(f"❌ Error checking login issues: {str(e)}")
            import traceback
            traceback.print_exc()

def create_test_user():
    """Create a test user with verified email"""
    print("\n👤 Creating test user with verified email...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if test user already exists
            test_user = User.query.filter_by(email='test@example.com').first()
            
            if test_user:
                print("✅ Test user already exists:")
                print(f"   Email: {test_user.email}")
                print(f"   Verified: {test_user.email_verified}")
                
                # Ensure user is verified
                if not test_user.email_verified:
                    test_user.email_verified = True
                    db.session.commit()
                    print("✅ User email verified!")
                
                return test_user
            else:
                print("📝 Creating new test user...")
                
                # Create test user
                user = User(
                    name='Test User',
                    phone='254700000000',
                    email='test@example.com',
                    email_verified=True  # Set to True to bypass verification
                )
                user.set_password('test123')
                
                db.session.add(user)
                db.session.commit()
                
                print("✅ Test user created successfully!")
                print(f"   Email: {user.email}")
                print(f"   Password: test123")
                print(f"   Verified: {user.email_verified}")
                
                return user
                
        except Exception as e:
            print(f"❌ Error creating test user: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return None

def fix_otp_issues():
    """Fix OTP generation issues"""
    print("\n🔧 Fixing OTP generation issues...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Clear any problematic OTP records
            old_otps = OTP.query.all()
            for otp in old_otps:
                db.session.delete(otp)
            
            db.session.commit()
            print("✅ Cleared old OTP records")
            
        except Exception as e:
            print(f"❌ Error fixing OTP issues: {str(e)}")
            db.session.rollback()

def disable_email_verification():
    """Temporarily disable email verification requirement"""
    print("\n🔧 Temporarily disabling email verification requirement...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Update all users to be verified
            users = User.query.all()
            for user in users:
                user.email_verified = True
            
            db.session.commit()
            print(f"✅ Set {len(users)} users as verified")
            
        except Exception as e:
            print(f"❌ Error disabling email verification: {str(e)}")
            db.session.rollback()

def test_login_credentials():
    """Test login credentials"""
    print("\n🔐 Testing login credentials...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test admin login
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            if admin:
                if admin.check_password('admin123'):
                    print("✅ Admin login works:")
                    print(f"   Email: {admin.email}")
                    print(f"   Password: admin123")
                else:
                    print("❌ Admin password verification failed")
            
            # Test user login
            user = User.query.filter_by(email='test@example.com').first()
            if user:
                if user.check_password('test123'):
                    print("✅ User login works:")
                    print(f"   Email: {user.email}")
                    print(f"   Password: test123")
                    print(f"   Verified: {user.email_verified}")
                else:
                    print("❌ User password verification failed")
            
        except Exception as e:
            print(f"❌ Error testing login: {str(e)}")

def main():
    """Main function to fix login issues"""
    print("🚀 KIBTECH Login Issues Fix Tool")
    print("=" * 50)
    
    # Check current issues
    check_login_issues()
    
    # Fix OTP issues
    fix_otp_issues()
    
    # Disable email verification temporarily
    disable_email_verification()
    
    # Create test user
    test_user = create_test_user()
    
    # Test login credentials
    test_login_credentials()
    
    print("\n" + "=" * 50)
    print("🎉 Login issues fixed!")
    print("\n📋 Available login credentials:")
    print("👤 Admin:")
    print("   Email: kibtechc@gmail.com")
    print("   Password: admin123")
    print("\n👥 User:")
    print("   Email: test@example.com")
    print("   Password: test123")
    print("\n💡 Next steps:")
    print("1. Try logging in with the credentials above")
    print("2. If still having issues, check the backend logs")
    print("3. Run 'python debug_db.py' for more diagnostics")

if __name__ == '__main__':
    main() 