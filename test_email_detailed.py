#!/usr/bin/env python3
"""
Detailed email service test
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_email_detailed():
    """Test email service with detailed logging"""
    
    print("🔍 Detailed Email Service Test")
    print("=" * 50)
    
    try:
        # Test Brevo service directly
        print("1. Testing Brevo service directly...")
        from app.services.brevo_service import get_brevo_service
        
        brevo_service = get_brevo_service()
        print("   ✅ Brevo service initialized")
        
        # Test email sending
        print("\n2. Testing email sending...")
        test_email = "emmkash20@gmail.com"  # Use a real email for testing
        test_otp = "123456"
        test_name = "Test User"
        
        result = brevo_service.send_email(
            to_email=test_email,
            subject="🔐 Test PIN Change - KibTech Store",
            html_content=f"""
            <h1>Test Email</h1>
            <p>Hello {test_name}!</p>
            <p>Your verification code is: <strong>{test_otp}</strong></p>
            <p>This is a test email to verify the email service is working.</p>
            """,
            text_content=f"Hello {test_name}! Your verification code is: {test_otp}",
            tags=['test', 'pin_change']
        )
        
        print(f"   Result: {result}")
        
        if result.get('success'):
            print("   ✅ Email sent successfully via Brevo API")
        else:
            print(f"   ❌ Email failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Brevo service test failed: {str(e)}")
        import traceback
        traceback.print_exc()

def test_email_service_integration():
    """Test the integrated email service"""
    
    print("\n3. Testing integrated email service...")
    
    try:
        from app.services.email_service import get_email_service
        
        email_service = get_email_service()
        print("   ✅ Email service initialized")
        
        # Test PIN change email
        test_email = "emmkash20@gmail.com"
        test_otp = "123456"
        test_name = "Test User"
        
        result = email_service.send_pin_change_verification(
            test_email, 
            test_otp, 
            test_name
        )
        
        print(f"   PIN change result: {result}")
        
        # Test PIN reset email
        result = email_service.send_pin_reset_verification(
            test_email, 
            test_otp, 
            test_name
        )
        
        print(f"   PIN reset result: {result}")
        
    except Exception as e:
        print(f"❌ Integrated email service test failed: {str(e)}")
        import traceback
        traceback.print_exc()

def check_configuration():
    """Check email configuration"""
    
    print("\n4. Checking email configuration...")
    
    try:
        from app.services.email_service import get_email_service
        
        email_service = get_email_service()
        
        print("   Configuration:")
        print(f"   - SMTP Server: {email_service.smtp_server}")
        print(f"   - SMTP Port: {email_service.smtp_port}")
        print(f"   - SMTP Username: {email_service.smtp_username}")
        print(f"   - Default Sender: {email_service.default_sender}")
        print(f"   - Use Brevo API: {email_service._use_brevo_api}")
        
        # Check if Brevo API key is available
        from flask import current_app
        brevo_key = current_app.config.get('BREVO_API_KEY')
        if brevo_key:
            print(f"   - Brevo API Key: {brevo_key[:20]}...")
        else:
            print("   - Brevo API Key: Not found")
            
    except Exception as e:
        print(f"❌ Configuration check failed: {str(e)}")

if __name__ == "__main__":
    print("🔧 Detailed Email Service Test")
    print("=" * 60)
    
    # Check configuration
    check_configuration()
    
    # Test Brevo service directly
    test_email_detailed()
    
    # Test integrated service
    test_email_service_integration()
    
    print("\n🎉 Detailed email test completed!")
    print("\n📝 Summary:")
    print("- Check if emails were received")
    print("- Verify Brevo API is working")
    print("- Check spam folder if emails not received") 