#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def reset_user_password():
    """Reset password for kashdyke@gmail.com user"""
    app = create_app()
    
    with app.app_context():
        print("Resetting password for kashdyke@gmail.com...")
        
        user = User.query.filter_by(email='kashdyke@gmail.com').first()
        
        if not user:
            print("❌ User kashdyke@gmail.com not found")
            return
        
        print(f"Found user: {user.name} ({user.email})")
        print(f"Email verified: {user.email_verified}")
        
        # Set new password
        new_password = "password123"
        user.set_password(new_password)
        
        # Commit the change
        db.session.commit()
        
        print(f"✅ Password reset successfully to: {new_password}")
        
        # Verify the password works
        if user.check_password(new_password):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")

if __name__ == '__main__':
    reset_user_password() 