#!/usr/bin/env python3

import os
import sys
from flask import Flask
from app import create_app
from app.services.email_service import get_email_service
from app.services.brevo_service import get_brevo_service

def test_email_service():
    """Test the email service functionality"""
    
    print("🧪 Testing Email Service Configuration...")
    app = create_app()
    
    with app.app_context():
        try:
            # Test Brevo service initialization
            brevo_service = get_brevo_service()
            print(f"✅ Brevo service initialized")
            
            # Check API key from configuration
            api_key = app.config.get('BREVO_API_KEY')
            print(f"📧 API Key configured: {'Yes' if api_key else 'No'}")
            if api_key:
                print(f"🔑 API Key (masked): {api_key[:15]}...{api_key[-4:]}")
            else:
                print("❌ No API Key found in configuration")
            
            # Test email service
            email_service = get_email_service()
            print(f"✅ Email service initialized")
            print(f"📮 Default sender: {app.config.get('MAIL_DEFAULT_SENDER', 'Not configured')}")
            print(f"🏷️  Sender name: {app.config.get('MAIL_DEFAULT_SENDER_NAME', 'Not configured')}")
            
            # Test send OTP email (dry run)
            print("\n🚀 Testing OTP email send...")
            test_email = "emmkash20@gmail.com"  # Use the email from logs
            test_otp = "123456"
            
            result = email_service.send_otp_email(
                email=test_email,
                otp_code=test_otp,
                purpose="password_reset",
                user_name="Test User"
            )
            
            print(f"📬 Email send result: {result}")
            
            if isinstance(result, dict):
                if result.get('success'):
                    print("✅ Email sent successfully!")
                    print(f"📨 Message ID: {result.get('message_id', 'N/A')}")
                else:
                    print(f"❌ Email failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"📮 Email result (boolean): {result}")
                
        except Exception as e:
            print(f"❌ Error testing email service: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_email_service()