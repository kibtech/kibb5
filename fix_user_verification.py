#!/usr/bin/env python3
from app import create_app, db
from app.models import User

def fix_user_verification():
    """Check and fix user verification status"""
    
    app = create_app()
    
    with app.app_context():
        # Get all users
        users = User.query.all()
        
        print(f"Found {len(users)} users in database")
        
        for user in users:
            print(f"\nUser: {user.email}")
            print(f"  Name: {user.name}")
            print(f"  Email Verified: {user.email_verified}")
            print(f"  Created: {user.created_at}")
            
            # Check if user has any OTP records for email verification
            email_otps = user.otps.filter_by(purpose='email_verification', is_used=True).all()
            print(f"  Email verification OTPs used: {len(email_otps)}")
            
            # If user has used email verification OTPs, they should be verified
            if email_otps and not user.email_verified:
                print(f"  ❌ User should be verified but isn't - fixing...")
                user.email_verified = True
                db.session.commit()
                print(f"  ✅ Fixed: {user.email} is now verified")
            elif not email_otps and user.email_verified:
                print(f"  ❌ User is verified but has no verification OTPs - unverifying...")
                user.email_verified = False
                db.session.commit()
                print(f"  ✅ Fixed: {user.email} is now unverified")
            else:
                print(f"  ✅ Status is correct")

if __name__ == '__main__':
    fix_user_verification() 