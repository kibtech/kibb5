#!/usr/bin/env python3
"""
Test email service within Flask application context
"""
from app import create_app
from app.services.email_service import get_email_service
from app.services.brevo_service import get_brevo_service

def test_email_with_context():
    """Test email service within Flask app context"""
    
    print("🔧 Testing Email Service with Flask Context")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            print("1. Testing Brevo service...")
            brevo_service = get_brevo_service()
            print("   ✅ Brevo service initialized")
            
            # Test direct Brevo email
            print("\n2. Testing direct Brevo email...")
            test_email = "emmkash20@gmail.com"
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
            
            # Test integrated email service
            print("\n3. Testing integrated email service...")
            email_service = get_email_service()
            print("   ✅ Email service initialized")
            
            # Test PIN change email
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
            
            # Check configuration
            print("\n4. Email configuration:")
            print(f"   - SMTP Server: {email_service.smtp_server}")
            print(f"   - SMTP Port: {email_service.smtp_port}")
            print(f"   - SMTP Username: {email_service.smtp_username}")
            print(f"   - Default Sender: {email_service.default_sender}")
            print(f"   - Use Brevo API: {email_service._use_brevo_api}")
            
            # Check Brevo API key
            from flask import current_app
            brevo_key = current_app.config.get('BREVO_API_KEY')
            if brevo_key:
                print(f"   - Brevo API Key: {brevo_key[:20]}...")
            else:
                print("   - Brevo API Key: Not found")
            
            print("\n🎉 Email service test completed successfully!")
            
        except Exception as e:
            print(f"❌ Email service test failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_email_with_context()
    
    print("\n📝 Summary:")
    print("- Check if emails were received at emmkash20@gmail.com")
    print("- Verify Brevo API is working correctly")
    print("- Check spam folder if emails not received")
    print("- The PIN change functionality should now work in the application") 