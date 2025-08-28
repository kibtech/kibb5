#!/usr/bin/env python3
"""
Test OTP Sending - Verify the complete flow
"""

import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_otp_sending():
    """Test OTP sending functionality"""
    
    print("🧪 Testing OTP Sending Functionality")
    print("=" * 50)
    
    try:
        from app import create_app, db
        from app.models import User
        from app.services.otp_service import get_otp_service
        
        app = create_app()
        
        with app.app_context():
            # Test 1: Check if we have any users
            users = User.query.all()
            print(f"📊 Found {len(users)} users in database")
            
            if users:
                # Test with the first user
                test_user = users[0]
                print(f"🧪 Testing with user: {test_user.email}")
                
                # Test OTP service
                otp_service = get_otp_service()
                
                # Send verification OTP
                print("\n📧 Sending verification OTP...")
                success, message = otp_service.send_email_verification_otp(test_user)
                
                if success:
                    print("✅ OTP sent successfully!")
                    print(f"📝 Message: {message}")
                    
                    # Check if OTP was stored in database
                    from app.models import OTP
                    otps = OTP.query.filter_by(user_id=test_user.id, purpose='email_verification').all()
                    print(f"📊 Found {len(otps)} OTP records for this user")
                    
                    if otps:
                        latest_otp = otps[-1]
                        print(f"🔢 Latest OTP: {latest_otp.otp_code}")
                        print(f"⏰ Expires at: {latest_otp.expires_at}")
                        print(f"📧 Purpose: {latest_otp.purpose}")
                        
                        # Test verification
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
                        print("⚠️ No OTP records found in database")
                else:
                    print("❌ Failed to send OTP")
                    print(f"📝 Error: {message}")
            else:
                print("⚠️ No users found in database")
                print("💡 Create a user first by registering")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_otp_sending() 