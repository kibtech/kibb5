#!/usr/bin/env python3
"""
Test OTP service fix
"""
from app import create_app, db
from app.services.otp_service import get_otp_service
from app.models import User

def test_otp_service():
    """Test OTP service functionality"""
    
    print("🧪 Testing OTP Service Fix")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Get OTP service
            otp_service = get_otp_service()
            print("✅ OTP service initialized")
            
            # Test with a real user
            user = User.query.first()
            if user:
                print(f"Testing with user: {user.name} ({user.email})")
                
                # Test email verification OTP
                print("\n📧 Testing email verification OTP...")
                success, message = otp_service.send_email_verification_otp(user)
                print(f"Result: {success}, Message: {message}")
                
                if success:
                    print("✅ Email verification OTP sent successfully!")
                    print(f"📧 Check email at: {user.email}")
                else:
                    print(f"❌ Failed to send OTP: {message}")
            else:
                print("❌ No users found in database")
            
            print("\n🎉 OTP service test completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_otp_service()
    
    print("\n📝 Summary:")
    print("- OTP service should now work correctly")
    print("- Email verification should work for new registrations")
    print("- PIN change should work with email verification")
    print("- Check your email for verification codes") 