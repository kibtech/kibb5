#!/usr/bin/env python3
"""
Simple Test for Commission Notification Email
"""

import requests
import json

# Configuration
base_url = "http://localhost:5000"

def test_commission_email():
    """Test the commission notification email"""
    print("🧪 Testing Commission Notification Email")
    print("=" * 40)
    
    try:
        # Step 1: Login as admin
        print("\n1. 🔐 Logging in as admin...")
        admin_login_data = {
            "email": "kibtechc@gmail.com",
            "password": "admin123"
        }
        
        admin_response = requests.post(f"{base_url}/api/auth/login", json=admin_login_data)
        
        if admin_response.status_code != 200:
            print(f"❌ Admin login failed: {admin_response.status_code}")
            return
        
        admin_token = admin_response.json().get('access_token')
        print("✅ Admin login successful")
        
        # Step 2: Test commission notification email
        print("\n2. 📧 Testing Commission Notification Email...")
        
        test_data = {
            "to_email": "test@example.com",  # Replace with your email
            "referrer_name": "John Doe",
            "commission_amount": 500.00,
            "order_details": {
                "order_number": "ORD-2024-001",
                "total_amount": 2500.00,
                "created_at": "December 15, 2024 at 2:30 PM"
            },
            "referred_user_name": "Jane Smith"
        }
        
        commission_response = requests.post(
            f"{base_url}/admin/email/test-commission-notification", 
            json=test_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        print(f"Status: {commission_response.status_code}")
        print(f"Response: {commission_response.text}")
        
        if commission_response.status_code == 200:
            print("✅ Commission notification email sent successfully!")
            print("📧 Check your email for the commission notification")
        else:
            print("❌ Commission notification email failed")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_commission_email() 