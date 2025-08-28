#!/usr/bin/env python3
"""
Test OTP expiration fix
"""
from app import create_app, db
from app.models import OTP
from datetime import datetime, timedelta

def test_otp_creation():
    """Test OTP creation with expiration"""
    
    print("🧪 Testing OTP Creation with Expiration")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Create a new OTP
            otp = OTP(
                user_id=1,
                email="test@example.com",
                purpose="pin_change"
            )
            
            # Generate OTP
            otp.generate_otp()
            
            print(f"OTP Code: {otp.otp_code}")
            print(f"Expires At: {otp.expires_at}")
            print(f"Is Valid: {otp.is_valid}")
            print(f"Is Expired: {otp.is_expired}")
            
            if otp.expires_at:
                print("✅ OTP expiration is set correctly!")
            else:
                print("❌ OTP expiration is still null")
            
            # Test saving to database
            db.session.add(otp)
            db.session.commit()
            print("✅ OTP saved to database successfully!")
            
            # Clean up
            db.session.delete(otp)
            db.session.commit()
            print("✅ Test OTP cleaned up")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_otp_creation()
    
    print("\n📝 Summary:")
    print("- OTP expiration should now be set automatically")
    print("- PIN change functionality should work")
    print("- Try changing PIN in the frontend again") 