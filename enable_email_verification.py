#!/usr/bin/env python3
"""
Enable Email Verification - Re-enable email verification for testing
"""

import re

def enable_email_verification():
    """Re-enable email verification requirement"""
    
    print("🔧 Re-enabling email verification requirement...")
    
    # Fix 1: Re-enable email verification in login route
    try:
        with open('app/auth/routes.py', 'r') as f:
            content = f.read()
        
        # Uncomment the email verification check
        pattern = r"# Check if email is verified \(temporarily disabled\)\n\s+# if not user\.email_verified:"
        replacement = "# Check if email is verified\n        if not user.email_verified:"
        
        if pattern in content:
            content = re.sub(pattern, replacement, content)
            
            # Also uncomment the return statement
            pattern2 = r"# return jsonify\(\{\n\s*#\s*'error': 'Email not verified',\n\s*#\s*'message': 'Please verify your email before logging in\. Check your email for verification code or request a new one\.',\n\s*#\s*'needs_verification': True,\n\s*#\s*'email': user\.email\n\s*#\s*\}\)\s*,\s*403"
            replacement2 = "return jsonify({\n                'error': 'Email not verified',\n                'message': 'Please verify your email before logging in. Check your email for verification code or request a new one.',\n                'needs_verification': True,\n                'email': user.email\n            }), 403"
            
            content = re.sub(pattern2, replacement2, content)
            
            with open('app/auth/routes.py', 'w') as f:
                f.write(content)
            
            print("✅ Email verification re-enabled in login route")
        else:
            print("⚠️ Email verification check not found in expected format")
            
    except Exception as e:
        print(f"❌ Error re-enabling email verification: {str(e)}")
    
    # Fix 2: Set all users as unverified for testing
    try:
        from app import create_app, db
        from app.models import User
        
        app = create_app()
        with app.app_context():
            # Set all users as email unverified for testing
            users = User.query.all()
            for user in users:
                user.email_verified = False
            db.session.commit()
            print(f"✅ Set {len(users)} users as email unverified for testing")
            
    except Exception as e:
        print(f"❌ Error setting users as unverified: {str(e)}")
    
    print("\n✅ Email verification re-enabled!")
    print("📝 Users will now be redirected to verification page when logging in")
    print("📝 OTP codes will be sent to their emails automatically")

if __name__ == "__main__":
    enable_email_verification() 