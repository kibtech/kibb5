#!/usr/bin/env python3
"""
Test Email Sending - Verify Brevo Integration
"""

import requests
import json
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_email_sending():
    """Test if email sending is working"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Email Sending Functionality")
    print("=" * 50)
    
    # Test 1: Register a new user (this should trigger email verification)
    print("\n📧 Testing User Registration (should trigger email verification)...")
    
    register_data = {
        "name": "Test User",
        "email": "test@example.com",  # Use your actual email here
        "password": "TestPassword123!",
        "phone": "1234567890"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/register", json=register_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ User registered successfully")
            print("📧 Check your email for verification code")
        else:
            print("❌ Registration failed")
            
    except Exception as e:
        print(f"❌ Error during registration: {e}")
    
    # Test 2: Test direct email sending via admin endpoint
    print("\n📧 Testing Direct Email Sending...")
    
    # First, we need to login as admin to access email endpoints
    admin_login_data = {
        "email": "kibtechc@gmail.com",
        "password": "Kibtechceo@2018"
    }
    
    try:
        # Login to admin portal
        admin_response = requests.post(f"{base_url}/admin/login", json=admin_login_data)
        print(f"Admin Login Status: {admin_response.status_code}")
        
        if admin_response.status_code == 200:
            print("✅ Admin login successful")
            
            # Test email sending
            test_email_data = {
                "email": "test@example.com",  # Use your actual email here
                "type": "otp"
            }
            
            email_response = requests.post(f"{base_url}/admin/email/test-email", json=test_email_data)
            print(f"Email Test Status: {email_response.status_code}")
            print(f"Email Test Response: {email_response.text}")
            
            if email_response.status_code == 200:
                print("✅ Test email sent successfully")
            else:
                print("❌ Test email failed")
        else:
            print("❌ Admin login failed")
            
    except Exception as e:
        print(f"❌ Error during email test: {e}")
    
    # Test 3: Check email configuration
    print("\n⚙️ Testing Email Configuration...")
    
    try:
        config_response = requests.get(f"{base_url}/admin/email/config")
        print(f"Config Status: {config_response.status_code}")
        
        if config_response.status_code == 200:
            config_data = config_response.json()
            print("✅ Email Configuration:")
            print(f"   - Brevo API Configured: {config_data.get('data', {}).get('brevo_api_configured')}")
            print(f"   - SMTP Configured: {config_data.get('data', {}).get('smtp_configured')}")
            print(f"   - API Connection: {config_data.get('data', {}).get('api_connection')}")
            print(f"   - Default Sender: {config_data.get('data', {}).get('default_sender')}")
        else:
            print("❌ Could not fetch email configuration")
            
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
    
    # Test 4: Check email health
    print("\n🏥 Testing Email Health...")
    
    try:
        health_response = requests.get(f"{base_url}/admin/email/health")
        print(f"Health Status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ Email Health Status:")
            print(f"   - Overall Status: {health_data.get('data', {}).get('overall_status')}")
            print(f"   - Brevo API: {health_data.get('data', {}).get('services', {}).get('brevo_api', {}).get('status')}")
            print(f"   - SMTP: {health_data.get('data', {}).get('services', {}).get('smtp', {}).get('status')}")
        else:
            print("❌ Could not fetch health status")
            
    except Exception as e:
        print(f"❌ Error checking health: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Summary:")
    print("1. If registration worked, check your email for verification code")
    print("2. If admin login worked, test emails should be sent")
    print("3. Check the configuration and health status above")
    print("4. If emails aren't being sent, check Brevo API key and SMTP settings")

if __name__ == "__main__":
    test_email_sending() 