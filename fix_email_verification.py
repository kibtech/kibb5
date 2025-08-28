#!/usr/bin/env python3
"""
Fix Email Verification - Temporarily disable for testing
"""

import re

def disable_email_verification():
    """Temporarily disable email verification requirement"""
    
    print("🔧 Temporarily disabling email verification requirement...")
    
    # Fix 1: Disable email verification in login route
    try:
        with open('app/auth/routes.py', 'r') as f:
            content = f.read()
        
        # Comment out the email verification check
        pattern = r"# Check if email is verified\n\s+if not user\.email_verified:"
        replacement = "# Check if email is verified (temporarily disabled)\n        # if not user.email_verified:"
        
        if pattern in content:
            content = re.sub(pattern, replacement, content)
            
            # Also comment out the return statement
            pattern2 = r"return jsonify\(\{\s*'error': 'Email not verified',\s*'message': 'Please verify your email before logging in\. Check your email for verification code or request a new one\.',\s*'needs_verification': True,\s*'email': user\.email\s*\}\)\s*,\s*403"
            replacement2 = "# return jsonify({\n            #     'error': 'Email not verified',\n            #     'message': 'Please verify your email before logging in. Check your email for verification code or request a new one.',\n            #     'needs_verification': True,\n            #     'email': user.email\n            # }), 403"
            
            content = re.sub(pattern2, replacement2, content)
            
            with open('app/auth/routes.py', 'w') as f:
                f.write(content)
            
            print("✅ Email verification disabled in login route")
        else:
            print("⚠️ Email verification check not found in expected format")
            
    except Exception as e:
        print(f"❌ Error disabling email verification: {str(e)}")
    
    # Fix 2: Set all existing users as verified
    try:
        from app import create_app, db
        from app.models import User
        
        app = create_app()
        with app.app_context():
            # Set all users as email verified
            users = User.query.all()
            for user in users:
                user.email_verified = True
            db.session.commit()
            print(f"✅ Set {len(users)} users as email verified")
            
    except Exception as e:
        print(f"❌ Error setting users as verified: {str(e)}")
    
    print("\n✅ Email verification temporarily disabled!")
    print("📝 Users can now login without email verification")
    print("📝 You can still test the email verification flow manually")

if __name__ == "__main__":
    disable_email_verification() 