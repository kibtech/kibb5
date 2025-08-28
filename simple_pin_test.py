#!/usr/bin/env python3
"""
Simple PIN change email test without database
"""
from app.services.email_service import get_email_service

def test_email_service():
    """Test email service directly"""
    
    print("🧪 Testing Email Service Directly")
    print("=" * 50)
    
    try:
        # Initialize email service
        print("1. Initializing email service...")
        email_service = get_email_service()
        print("   ✅ Email service initialized")
        
        # Test PIN change email
        print("\n2. Testing PIN change email...")
        test_email = "test@example.com"
        test_otp = "123456"
        test_name = "Test User"
        
        result = email_service.send_pin_change_verification(
            test_email, 
            test_otp, 
            test_name
        )
        print(f"   ✅ PIN change email sent: {result}")
        
        # Test PIN reset email
        print("\n3. Testing PIN reset email...")
        result = email_service.send_pin_reset_verification(
            test_email, 
            test_otp, 
            test_name
        )
        print(f"   ✅ PIN reset email sent: {result}")
        
        print("\n🎉 Email service test completed successfully!")
        
    except Exception as e:
        print(f"❌ Email service test failed: {str(e)}")
        import traceback
        traceback.print_exc()

def check_email_config():
    """Check email configuration"""
    
    print("\n📧 Email Configuration Check")
    print("=" * 50)
    
    try:
        email_service = get_email_service()
        
        print("Email Service Properties:")
        print(f"   SMTP Server: {email_service.smtp_server}")
        print(f"   SMTP Port: {email_service.smtp_port}")
        print(f"   SMTP Username: {email_service.smtp_username}")
        print(f"   Default Sender: {email_service.default_sender}")
        print(f"   Default Sender Name: {email_service.default_sender_name}")
        print(f"   Use Brevo API: {email_service._use_brevo_api}")
        
        print("\n✅ Email configuration loaded successfully!")
        
    except Exception as e:
        print(f"❌ Email configuration check failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔧 Simple PIN Change Email Test")
    print("=" * 60)
    
    # Check email configuration
    check_email_config()
    
    # Test email service
    test_email_service()
    
    print("\n🎉 All tests completed!")
    print("\n📝 Next Steps:")
    print("1. Check if emails were sent to test@example.com")
    print("2. Verify Brevo email service is working")
    print("3. Test with real user email in the application") 