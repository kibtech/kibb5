#!/usr/bin/env python3
from app import create_app
from app.services.brevo_service import get_brevo_service

def test_brevo_service():
    """Test Brevo email service"""
    
    app = create_app()
    
    with app.app_context():
        print("Testing Brevo service...")
        
        brevo_service = get_brevo_service()
        
        # Test sending a simple email
        test_email = "test@example.com"
        test_subject = "Test Email from KibTech"
        test_html = """
        <html>
        <body>
            <h1>Test Email</h1>
            <p>This is a test email from KibTech to verify the email service is working.</p>
            <p>If you receive this email, the email service is configured correctly.</p>
        </body>
        </html>
        """
        
        try:
            result = brevo_service.send_email(
                to_email=test_email,
                subject=test_subject,
                html_content=test_html,
                tags=['test', 'kibtech']
            )
            
            print(f"Brevo service result: {result}")
            
            if result.get('success'):
                print("✅ Brevo service is working")
            else:
                print(f"❌ Brevo service failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Brevo service error: {e}")

if __name__ == '__main__':
    test_brevo_service() 