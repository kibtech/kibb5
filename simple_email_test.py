#!/usr/bin/env python3
"""
Simple Email Test - Test email sending with proper Flask context
"""

import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_email_simple():
    """Simple email test with Flask context"""
    
    print("🧪 Simple Email Test")
    print("=" * 50)
    
    try:
        from app import create_app
        from app.services.otp_service import get_otp_service
        from app.models import User
        
        print("✅ Successfully imported Flask app and services")
        
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            # Test 1: Check if we have users
            users = User.query.all()
            print(f"📊 Found {len(users)} users in database")
            
            if not users:
                print("⚠️ No users found. Creating a test user...")
                
                # Create a test user
                test_user = User(
                    name="Test User",
                    email="kibtechc@gmail.com",  # Using your email for testing
                    phone="1234567890"
                )
                test_user.set_password("TestPassword123!")
                
                from app import db
                db.session.add(test_user)
                db.session.commit()
                print("✅ Created test user")
            else:
                test_user = users[0]
                print(f"🧪 Using existing user: {test_user.email}")
            
            # Test 2: Send OTP email
            print("\n📧 Sending OTP email...")
            otp_service = get_otp_service()
            
            success, message = otp_service.send_email_verification_otp(test_user)
            
            if success:
                print("✅ OTP email sent successfully!")
                print(f"📝 Message: {message}")
                
                # Test 3: Check OTP in database
                from app.models import OTP
                otps = OTP.query.filter_by(user_id=test_user.id, purpose='email_verification').all()
                
                if otps:
                    latest_otp = otps[-1]
                    print(f"🔢 OTP Code: {latest_otp.otp_code}")
                    print(f"⏰ Expires: {latest_otp.expires_at}")
                    print(f"📧 Purpose: {latest_otp.purpose}")
                    
                    # Test 4: Verify OTP
                    print("\n🔍 Testing OTP verification...")
                    verify_success, verify_message = otp_service.verify_email_verification(
                        test_user.email, 
                        latest_otp.otp_code
                    )
                    
                    if verify_success:
                        print("✅ OTP verification successful!")
                        print(f"📝 Message: {verify_message}")
                    else:
                        print("❌ OTP verification failed")
                        print(f"📝 Error: {verify_message}")
                else:
                    print("⚠️ No OTP found in database")
            else:
                print("❌ Failed to send OTP email")
                print(f"📝 Error: {message}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email_simple() 