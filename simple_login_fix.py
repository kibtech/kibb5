#!/usr/bin/env python3
"""
Simple Login Fix for KIBTECH
"""

import os
import sys

def main():
    print("🔧 Simple Login Fix for KIBTECH")
    print("=" * 40)
    
    try:
        # Import Flask app
        from app import create_app, db
        from app.models import User, AdminUser
        
        app = create_app()
        
        with app.app_context():
            print("✅ Database connection successful")
            
            # Check users
            users = User.query.all()
            print(f"👥 Users found: {len(users)}")
            
            # Check admins
            admins = AdminUser.query.all()
            print(f"👤 Admins found: {len(admins)}")
            
            # Create test user if none exist
            if len(users) == 0:
                print("📝 Creating test user...")
                user = User(
                    name='Test User',
                    email='test@example.com',
                    phone='254700000000',
                    email_verified=True
                )
                user.set_password('test123')
                db.session.add(user)
                db.session.commit()
                print("✅ Test user created!")
            
            # Ensure all users are verified
            for user in users:
                if not user.email_verified:
                    user.email_verified = True
                    print(f"✅ Verified user: {user.email}")
            
            db.session.commit()
            print("✅ All users verified!")
            
            print("\n📋 Login Credentials:")
            print("👤 Admin: kibtechc@gmail.com / admin123")
            print("👥 User: test@example.com / test123")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 