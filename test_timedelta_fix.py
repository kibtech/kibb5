#!/usr/bin/env python3
"""
Test timedelta fix for OTP model
"""
from app import create_app, db
from app.models import OTP

def test_timedelta_fix():
    """Test that timedelta is now available in OTP model"""
    
    print("🧪 Testing Timedelta Fix")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Test creating OTP
            otp = OTP(
                user_id=1,
                email="test@example.com",
                purpose="test"
            )
            
            # Generate OTP (this should now work with timedelta)
            otp.generate_otp()
            
            print(f"✅ OTP created successfully!")
            print(f"   OTP Code: {otp.otp_code}")
            print(f"   Expires At: {otp.expires_at}")
            print(f"   Is Valid: {otp.is_valid}")
            
            if otp.expires_at:
                print("✅ OTP expiration is set correctly!")
            else:
                print("❌ OTP expiration is still null")
            
            print("\n🎉 Timedelta fix test completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_timedelta_fix()
    
    print("\n📝 Summary:")
    print("- Timedelta should now be available in OTP model")
    print("- OTP expiration should be set correctly")
    print("- PIN change and email verification should work")
    print("- Try registering a new user or changing PIN again") 