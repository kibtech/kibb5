#!/usr/bin/env python3
"""
Test script for commission notification emails
This script tests the commission notification functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.email_service import get_email_service
from decimal import Decimal

def test_commission_notification():
    """Test the commission notification email functionality"""
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            # Get email service
            email_service = get_email_service()
            
            # Test data
            test_data = {
                'to_email': 'test@example.com',  # Replace with actual test email
                'referrer_name': 'John Doe',
                'commission_amount': 500.00,
                'order_details': {
                    'order_number': 'ORD-2024-001',
                    'total_amount': 2500.00,
                    'created_at': 'December 15, 2024 at 2:30 PM',
                    'item_count': 3
                },
                'referred_user_name': 'Jane Smith'
            }
            
            print("🧪 Testing Commission Notification Email...")
            print(f"📧 Sending to: {test_data['to_email']}")
            print(f"👤 Referrer: {test_data['referrer_name']}")
            print(f"💰 Commission: KSh {test_data['commission_amount']:.2f}")
            print(f"🛒 Order: #{test_data['order_details']['order_number']}")
            print(f"👥 Referred User: {test_data['referred_user_name']}")
            
            # Send commission notification
            result = email_service.send_commission_notification(
                to_email=test_data['to_email'],
                referrer_name=test_data['referrer_name'],
                commission_amount=test_data['commission_amount'],
                order_details=test_data['order_details'],
                referred_user_name=test_data['referred_user_name']
            )
            
            if isinstance(result, dict) and result.get('success'):
                print("✅ Commission notification email sent successfully!")
                print(f"📨 Message ID: {result.get('message_id', 'N/A')}")
                return True
            elif result is True:
                print("✅ Commission notification email sent successfully via SMTP!")
                return True
            else:
                print("❌ Failed to send commission notification email")
                print(f"Error: {result}")
                return False
        
    except Exception as e:
            print(f"❌ Error testing commission notification: {str(e)}")
            return False

if __name__ == "__main__":
    print("🚀 Commission Notification Email Test")
    print("=" * 50)
    
    # Test with sample data
    print("\n1. Testing with sample data...")
    test_commission_notification() 
    
    print("\n✅ Commission notification test completed!") 