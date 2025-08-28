#!/usr/bin/env python3
"""
Standalone B2C Test
This script tests the B2C system without requiring Flask application context
"""

import os
import sys
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the ngrok URL for testing
NGROK_URL = "https://65db561a00a0.ngrok-free.app"

def setup_ngrok_environment():
    """Set up environment variables for ngrok testing"""
    print("🔧 Setting up ngrok environment for testing...")
    
    # Update environment variables to use ngrok URLs
    os.environ['MPESA_RESULT_URL'] = f"{NGROK_URL}/api/mpesa/b2c-result"
    os.environ['MPESA_TIMEOUT_URL'] = f"{NGROK_URL}/api/mpesa/timeout"
    os.environ['MPESA_CALLBACK_URL'] = f"{NGROK_URL}/api/mpesa/callback"
    
    print(f"✅ Updated callback URLs to use ngrok:")
    print(f"   Result URL: {os.environ['MPESA_RESULT_URL']}")
    print(f"   Timeout URL: {os.environ['MPESA_TIMEOUT_URL']}")
    print(f"   Callback URL: {os.environ['MPESA_CALLBACK_URL']}")

def check_configuration():
    """Check your system configuration"""
    print(f"\n🔍 Checking your system configuration...")
    
    config_vars = {
        'MPESA_CONSUMER_KEY': os.environ.get('MPESA_CONSUMER_KEY'),
        'MPESA_CONSUMER_SECRET': os.environ.get('MPESA_CONSUMER_SECRET'),
        'MPESA_SHORTCODE': os.environ.get('MPESA_SHORTCODE'),
        'MPESA_PASSKEY': os.environ.get('MPESA_PASSKEY'),
        'MPESA_INITIATOR_NAME': os.environ.get('MPESA_INITIATOR_NAME'),
        'MPESA_INITIATOR_PASSWORD': os.environ.get('MPESA_INITIATOR_PASSWORD'),
        'MPESA_SECURITY_CREDENTIAL': os.environ.get('MPESA_SECURITY_CREDENTIAL'),
        'MPESA_BASE_URL': os.environ.get('MPESA_BASE_URL')
    }
    
    print(f"📋 Your configuration:")
    for var_name, value in config_vars.items():
        if value:
            print(f"   {var_name}: ✅ Set ({len(value)} chars)")
        else:
            print(f"   {var_name}: ❌ Not set")
    
    required_fields = [
        'MPESA_CONSUMER_KEY', 'MPESA_CONSUMER_SECRET', 'MPESA_SHORTCODE',
        'MPESA_PASSKEY', 'MPESA_INITIATOR_NAME', 'MPESA_INITIATOR_PASSWORD',
        'MPESA_SECURITY_CREDENTIAL', 'MPESA_BASE_URL'
    ]
    
    missing_fields = []
    for field in required_fields:
        if not config_vars.get(field):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"\n❌ Missing required fields: {', '.join(missing_fields)}")
        return False
    else:
        print(f"\n✅ All required fields are configured!")
        return True

def test_ngrok_connectivity():
    """Test if ngrok tunnel is accessible"""
    print(f"\n🌐 Testing ngrok connectivity...")
    
    try:
        response = requests.get(f"{NGROK_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Ngrok tunnel is accessible!")
            return True
        else:
            print(f"⚠️ Ngrok responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach ngrok tunnel: {e}")
        print("💡 Make sure your ngrok tunnel is running and accessible")
        return False

def get_access_token():
    """Get OAuth access token from M-Pesa"""
    print(f"\n🔑 Getting OAuth access token...")
    
    consumer_key = os.environ.get('MPESA_CONSUMER_KEY')
    consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET')
    base_url = os.environ.get('MPESA_BASE_URL')
    
    if not all([consumer_key, consumer_secret, base_url]):
        print("❌ Missing required credentials for OAuth")
        return None
    
    # OAuth URL
    oauth_url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(
            oauth_url,
            auth=(consumer_key, consumer_secret),
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get('access_token')
            if access_token:
                print(f"✅ OAuth token acquired successfully")
                print(f"   Token: {access_token[:20]}...")
                return access_token
            else:
                print(f"❌ No access token in response")
                return None
        else:
            print(f"❌ OAuth request failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ OAuth request error: {e}")
        return None

def format_phone_number(phone):
    """Format phone number to 254XXXXXXXXX format"""
    # Remove any non-digit characters
    phone = ''.join(filter(str.isdigit, str(phone)))
    
    # Handle different formats
    if phone.startswith('0'):
        # 07XXXXXXXX -> 254XXXXXXXX
        return '254' + phone[1:]
    elif phone.startswith('+254'):
        # +254XXXXXXXX -> 254XXXXXXXX
        return phone[1:]
    elif phone.startswith('254'):
        # Already in correct format
        return phone
    else:
        # Assume it's already in correct format
        return phone

def test_b2c_payment():
    """Test B2C payment directly"""
    print(f"\n🧪 Testing B2C payment...")
    
    # Get access token
    access_token = get_access_token()
    if not access_token:
        print("❌ Cannot proceed without access token")
        return False
    
    # Get configuration
    shortcode = os.environ.get('MPESA_SHORTCODE')
    initiator_name = os.environ.get('MPESA_INITIATOR_NAME')
    security_credential = os.environ.get('MPESA_SECURITY_CREDENTIAL')
    base_url = os.environ.get('MPESA_BASE_URL')
    result_url = os.environ.get('MPESA_RESULT_URL')
    timeout_url = os.environ.get('MPESA_TIMEOUT_URL')
    
    # Test phone number
    test_phone = "0112735877"
    formatted_phone = format_phone_number(test_phone)
    
    print(f"📱 Phone: {test_phone} → {formatted_phone}")
    print(f"💰 Amount: 10 KES")
    print(f"🏢 Shortcode: {shortcode}")
    print(f"👤 Initiator: {initiator_name}")
    
    # B2C API URL
    b2c_url = f"{base_url}/mpesa/b2c/v1/paymentrequest"
    
    # Request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Request payload
    payload = {
        "InitiatorName": initiator_name,
        "SecurityCredential": security_credential,
        "CommandID": "BusinessPayment",
        "Amount": 10,
        "PartyA": shortcode,
        "PartyB": formatted_phone,
        "Remarks": "Test B2C Payment with Ngrok",
        "QueueTimeOutURL": timeout_url,
        "ResultURL": result_url,
        "Occasion": "Test Payment"
    }
    
    print(f"\n🚀 Sending B2C request...")
    print(f"   URL: {b2c_url}")
    print(f"   Result URL: {result_url}")
    print(f"   Timeout URL: {timeout_url}")
    
    try:
        response = requests.post(
            b2c_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\n📊 B2C Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 B2C Response: {json.dumps(data, indent=2)}")
            
            if 'ConversationID' in data:
                print(f"\n✅ SUCCESS! B2C payment initiated!")
                print(f"   Conversation ID: {data['ConversationID']}")
                if 'ResponseDescription' in data:
                    desc = data['ResponseDescription']
                    print(f"   Description: {desc}")
                
                print(f"\n🎉 B2C TEST SUCCESSFUL!")
                print(f"📱 Check your phone (0112735877) for the payment notification")
                print(f"📊 Monitor ngrok logs for callback results")
                print(f"🌐 Ngrok URL: {NGROK_URL}")
                
                return True
            else:
                print(f"\n❌ No ConversationID in response")
                return False
        else:
            print(f"\n❌ B2C request failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ B2C request error: {e}")
        return False

def show_test_instructions():
    """Show instructions for monitoring the test"""
    print(f"\n📋 Test Instructions:")
    print("=" * 50)
    print(f"1. 🌐 Your ngrok tunnel is running at: {NGROK_URL}")
    print(f"2. 📱 The test will send 10 KES to phone: 0112735877")
    print(f"3. 🔔 You should receive an M-Pesa notification on your phone")
    print(f"4. 📊 Check ngrok logs for callback results")
    print(f"5. 💰 If successful, you'll receive 10 KES on your phone")
    
    print(f"\n🔍 To monitor callbacks:")
    print(f"   - Check ngrok web interface: http://localhost:4040")
    print(f"   - Monitor your Flask app logs")
    print(f"   - Check your phone for M-Pesa notification")
    
    print(f"\n⚠️  Important Notes:")
    print(f"   - This is a REAL payment of 10 KES")
    print(f"   - Make sure 0112735877 is your correct phone number")
    print(f"   - The money will be deducted from your M-Pesa business account")

def main():
    """Main test function"""
    print("🧪 Standalone B2C Test")
    print("=" * 50)
    
    # Check configuration
    if not check_configuration():
        print(f"\n❌ Cannot proceed - missing required configuration")
        return False
    
    # Set up ngrok environment
    setup_ngrok_environment()
    
    # Test ngrok connectivity
    if not test_ngrok_connectivity():
        print(f"\n❌ Cannot proceed without ngrok connectivity")
        return False
    
    # Show test instructions
    show_test_instructions()
    
    # Ask for confirmation
    print(f"\n🤔 Do you want to proceed with the B2C test?")
    print(f"   This will send 10 KES to 0112735877")
    response = input("   Type 'yes' to continue: ").strip().lower()
    
    if response != 'yes':
        print(f"❌ Test cancelled by user")
        return False
    
    # Run the B2C test
    success = test_b2c_payment()
    
    # Summary
    print(f"\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    if success:
        print("✅ B2C test SUCCESSFUL!")
        print("🎉 Your B2C system is working correctly!")
        print("📱 Check your phone for the payment notification")
        print("📊 Monitor ngrok logs for callback results")
    else:
        print("❌ B2C test FAILED!")
        print("💡 Check the error messages above and fix the issues")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 