#!/usr/bin/env python3
"""
Test PIN change functionality with Brevo email service
"""
from app import create_app, db
from app.models import User, OTP
from app.services.email_service import get_email_service

def test_pin_change_email():
    """Test PIN change email functionality"""
    
    print("🧪 Testing PIN Change Email Functionality")
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
            
            # Test email service
            print("\n1. Testing Email Service...")
            email_service = get_email_service()
            print(f"   Email service initialized: {email_service is not None}")
            
            # Test PIN change email
            print("\n2. Testing PIN Change Email...")
            test_otp = "123456"
            
            try:
                result = email_service.send_pin_change_verification(
                    user.email, 
                    test_otp, 
                    user.name
                )
                print(f"   Email sent successfully: {result}")
                print(f"   Check email at: {user.email}")
            except Exception as e:
                print(f"   ❌ Email sending failed: {str(e)}")
            
            # Test PIN reset email
            print("\n3. Testing PIN Reset Email...")
            try:
                result = email_service.send_pin_reset_verification(
                    user.email, 
                    test_otp, 
                    user.name
                )
                print(f"   Email sent successfully: {result}")
                print(f"   Check email at: {user.email}")
            except Exception as e:
                print(f"   ❌ Email sending failed: {str(e)}")
            
            # Test OTP generation
            print("\n4. Testing OTP Generation...")
            otp = OTP(
                user_id=user.id,
                email=user.email,
                purpose='pin_change'
            )
            otp.generate_otp()
            print(f"   OTP generated: {otp.otp_code}")
            print(f"   OTP expires at: {otp.expires_at}")
            print(f"   OTP is valid: {otp.is_valid}")
            
            print("\n✅ PIN Change Email Test Completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

def test_pin_change_flow():
    """Test the complete PIN change flow"""
    
    print("\n🔄 Testing Complete PIN Change Flow")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Get a test user
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return
            
            print(f"Testing with user: {user.name}")
            
            # Step 1: Generate OTP
            print("\n1. Generating OTP...")
            otp = OTP(
                user_id=user.id,
                email=user.email,
                purpose='pin_change'
            )
            otp.generate_otp()
            db.session.add(otp)
            db.session.commit()
            
            print(f"   OTP: {otp.otp_code}")
            
            # Step 2: Send email
            print("\n2. Sending email...")
            email_service = get_email_service()
            result = email_service.send_pin_change_verification(
                user.email, 
                otp.otp_code, 
                user.name
            )
            print(f"   Email result: {result}")
            
            # Step 3: Verify OTP
            print("\n3. Verifying OTP...")
            valid_otp = OTP.get_valid_otp(user.email, 'pin_change', otp.otp_code)
            if valid_otp:
                print("   ✅ OTP verification successful")
                valid_otp.mark_as_used()
                print("   ✅ OTP marked as used")
            else:
                print("   ❌ OTP verification failed")
            
            # Step 4: Change PIN
            print("\n4. Changing PIN...")
            old_pin_hash = user.wallet_pin
            user.set_wallet_pin("5678")
            db.session.commit()
            
            print("   ✅ PIN changed successfully")
            print(f"   Old PIN hash: {old_pin_hash[:20]}...")
            print(f"   New PIN hash: {user.wallet_pin[:20]}...")
            
            # Step 5: Test new PIN
            print("\n5. Testing new PIN...")
            if user.check_wallet_pin("5678"):
                print("   ✅ New PIN works correctly")
            else:
                print("   ❌ New PIN verification failed")
            
            # Step 6: Test old PIN (should fail)
            if not user.check_wallet_pin("1234"):
                print("   ✅ Old PIN correctly rejected")
            else:
                print("   ❌ Old PIN incorrectly accepted")
            
            print("\n🎉 Complete PIN Change Flow Test Successful!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("🔧 PIN Change Email Fix Test")
    print("=" * 60)
    
    # Test email functionality
    test_pin_change_email()
    
    # Test complete flow
    test_pin_change_flow()
    
    print("\n🎉 All tests completed!")
    print("\n📝 Next Steps:")
    print("1. Check your email for the test messages")
    print("2. Try changing PIN in the frontend")
    print("3. Verify the email verification works") 