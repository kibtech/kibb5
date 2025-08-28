#!/usr/bin/env python3
"""
Quick Email Test - Test Brevo Integration Directly
"""

import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_brevo_directly():
    """Test Brevo email service directly"""
    
    print("🧪 Testing Brevo Email Service Directly")
    print("=" * 50)
    
    try:
        # Import Flask app and services
        from app import create_app
        from app.services.brevo_service import get_brevo_service
        from app.services.email_service import get_email_service
        
        print("✅ Successfully imported Flask app and email services")
        
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            # Test Brevo service
            print("\n📧 Testing Brevo Service...")
            brevo_service = get_brevo_service()
            
            # Test configuration
            print("🔧 Checking Brevo configuration...")
            try:
                config = brevo_service.configuration
                print(f"✅ Brevo configuration loaded")
                print(f"   - API Key configured: {'Yes' if config.api_key.get('api-key') else 'No'}")
            except Exception as e:
                print(f"❌ Configuration error: {e}")
                return
        
            # Test email sending
            print("\n📧 Testing email sending...")
            test_email = "test@example.com"  # Replace with your email
            
            try:
                result = brevo_service.send_otp_email(
                    email=test_email,
                    otp_code="123456",
                    purpose="verification",
                    user_name="Test User"
                )
                
                print(f"📧 Email send result: {result}")
                
                if result.get('success'):
                    print("✅ Email sent successfully!")
                    print(f"   - Message ID: {result.get('message_id')}")
                else:
                    print("❌ Email sending failed")
                    print(f"   - Error: {result.get('error')}")
                    
            except Exception as e:
                print(f"❌ Email sending error: {e}")
            
            # Test email service
            print("\n📧 Testing Email Service...")
            email_service = get_email_service()
            
            try:
                result = email_service.send_otp_email(
                    email=test_email,
                    otp_code="654321",
                    purpose="verification",
                    user_name="Test User"
                )
                
                print(f"📧 Email service result: {result}")
                
                if isinstance(result, dict) and result.get('success'):
                    print("✅ Email service working!")
                elif result is True:
                    print("✅ Email service working (SMTP fallback)")
                else:
                    print("❌ Email service failed")
                    
            except Exception as e:
                print(f"❌ Email service error: {e}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_brevo_directly() 