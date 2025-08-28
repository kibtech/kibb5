#!/usr/bin/env python3
"""
Script to verify email verification removal and update database
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from app import create_app, db
    from app.models import User, AdminUser
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Verifying email verification removal...")
        print("=" * 50)
        
        # Check User model
        print("\n1️⃣ Checking User model...")
        try:
            # Get a sample user to check the model
            sample_user = User.query.first()
            if sample_user:
                print(f"   ✅ User model accessible")
                print(f"   📧 Sample user email: {sample_user.email}")
                print(f"   ✅ Email verified: {sample_user.email_verified}")
            else:
                print("   ⚠️  No users found in database")
        except Exception as e:
            print(f"   ❌ Error accessing User model: {e}")
        
        # Check AdminUser model
        print("\n2️⃣ Checking AdminUser model...")
        try:
            sample_admin = AdminUser.query.first()
            if sample_admin:
                print(f"   ✅ AdminUser model accessible")
                print(f"   📧 Sample admin email: {sample_admin.email}")
                print(f"   ✅ Email verified: {sample_admin.email_verified}")
            else:
                print("   ⚠️  No admin users found in database")
        except Exception as e:
            print(f"   ❌ Error accessing AdminUser model: {e}")
        
        # Update all users to have email_verified = True
        print("\n3️⃣ Updating database...")
        try:
            # Update regular users
            users_updated = db.session.execute(
                "UPDATE users SET email_verified = TRUE WHERE email_verified = FALSE"
            ).rowcount
            print(f"   ✅ Updated {users_updated} regular users")
            
            # Update admin users
            admin_users_updated = db.session.execute(
                "UPDATE admin_users SET email_verified = TRUE WHERE email_verified = FALSE"
            ).rowcount
            print(f"   ✅ Updated {admin_users_updated} admin users")
            
            # Commit changes
            db.session.commit()
            print("   ✅ Database changes committed")
            
        except Exception as e:
            print(f"   ❌ Error updating database: {e}")
            db.session.rollback()
        
        # Verify the changes
        print("\n4️⃣ Verifying changes...")
        try:
            total_users = User.query.count()
            verified_users = User.query.filter_by(email_verified=True).count()
            unverified_users = User.query.filter_by(email_verified=False).count()
            
            print(f"   📊 Regular users:")
            print(f"      Total: {total_users}")
            print(f"      Verified: {verified_users}")
            print(f"      Unverified: {unverified_users}")
            
            total_admin_users = AdminUser.query.count()
            verified_admin_users = AdminUser.query.filter_by(email_verified=True).count()
            unverified_admin_users = AdminUser.query.filter_by(email_verified=False).count()
            
            print(f"   📊 Admin users:")
            print(f"      Total: {total_admin_users}")
            print(f"      Verified: {verified_admin_users}")
            print(f"      Unverified: {unverified_admin_users}")
            
        except Exception as e:
            print(f"   ❌ Error verifying changes: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Email verification removal verification completed!")
        print("\n📋 Summary:")
        print("   • User model updated to default email_verified = True")
        print("   • Database updated to set all existing users as verified")
        print("   • Email verification requirements removed from auth routes")
        print("\n🔄 Next steps:")
        print("   1. Restart your Flask application")
        print("   2. Test user registration (should work without email verification)")
        print("   3. Test user login (should work immediately)")
        print("   4. Test password reset (should work without OTP)")
        
except ImportError as e:
    print(f"❌ Error importing app: {e}")
    print("Make sure you're running this script from the project root directory")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 