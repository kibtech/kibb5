#!/usr/bin/env python3
"""
Test script to verify PIN reset functionality
"""
from app import create_app, db
from app.models import User, OTP
from datetime import datetime, timedelta

def test_pin_reset():
    """Test PIN reset functionality"""
    
    print("🔐 Testing PIN Reset Functionality")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Get a test user
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return
            
            print(f"Testing with user: {user.name} ({user.email})")
            
            # Check if user has PIN set
            if not user.has_wallet_pin():
                print("ℹ️  User doesn't have PIN set, setting one first...")
                user.set_wallet_pin("1234")
                db.session.commit()
                print("✅ PIN set successfully")
            
            print(f"Current PIN attempts: {user.pin_attempts}")
            print(f"PIN locked: {user.is_pin_locked()}")
            
            # Test PIN reset OTP generation
            print("\n1. Testing PIN Reset OTP Generation...")
            
            # Create OTP for PIN reset
            otp = OTP(
                user_id=user.id,
                email=user.email,
                purpose='pin_reset'
            )
            otp.generate_otp()
            db.session.add(otp)
            db.session.commit()
            
            print(f"✅ OTP generated: {otp.otp_code}")
            print(f"OTP expires at: {otp.expires_at}")
            print(f"OTP is valid: {otp.is_valid}")
            
            # Test OTP verification
            print("\n2. Testing OTP Verification...")
            
            # Test with correct OTP
            valid_otp = OTP.get_valid_otp(user.email, 'pin_reset', otp.otp_code)
            if valid_otp:
                print("✅ OTP verification successful")
                valid_otp.mark_as_used()
                print("✅ OTP marked as used")
            else:
                print("❌ OTP verification failed")
            
            # Test with wrong OTP
            invalid_otp = OTP.get_valid_otp(user.email, 'pin_reset', '999999')
            if not invalid_otp:
                print("✅ Invalid OTP correctly rejected")
            else:
                print("❌ Invalid OTP incorrectly accepted")
            
            # Test PIN reset functionality
            print("\n3. Testing PIN Reset...")
            
            # Simulate PIN reset
            old_pin_hash = user.wallet_pin
            user.set_wallet_pin("5678")
            user.pin_attempts = 0
            user.pin_locked_until = None
            db.session.commit()
            
            print("✅ PIN reset successfully")
            print(f"Old PIN hash: {old_pin_hash[:20]}...")
            print(f"New PIN hash: {user.wallet_pin[:20]}...")
            
            # Test new PIN
            if user.check_wallet_pin("5678"):
                print("✅ New PIN works correctly")
            else:
                print("❌ New PIN verification failed")
            
            # Test old PIN (should fail)
            if not user.check_wallet_pin("1234"):
                print("✅ Old PIN correctly rejected")
            else:
                print("❌ Old PIN incorrectly accepted")
            
            print("\n🎉 PIN Reset Test Completed Successfully!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            raise

if __name__ == "__main__":
    test_pin_reset() 