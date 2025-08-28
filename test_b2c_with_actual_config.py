#!/usr/bin/env python3
"""
Test B2C with Actual System Configuration
This script tests the B2C system using your actual environment variables
"""

import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the ngrok URL for testing
# Update this to your current ngrok URL
NGROK_URL = "https://65db561a00a0.ngrok-free.app"  # Your current ngrok URL

def setup_ngrok_environment():
    """Set up environment variables for ngrok testing using your actual config"""
    print("🔧 Setting up ngrok environment for testing...")
    
    # Update environment variables to use ngrok URLs (using your actual MPESA_ prefix)
    os.environ['MPESA_RESULT_URL'] = f"{NGROK_URL}/api/mpesa/b2c-result"
    os.environ['MPESA_TIMEOUT_URL'] = f"{NGROK_URL}/api/mpesa/timeout"
    os.environ['MPESA_CALLBACK_URL'] = f"{NGROK_URL}/api/mpesa/callback"
    
    print(f"✅ Updated callback URLs to use ngrok:")
    print(f"   Result URL: {os.environ['MPESA_RESULT_URL']}")
    print(f"   Timeout URL: {os.environ['MPESA_TIMEOUT_URL']}")
    print(f"   Callback URL: {os.environ['MPESA_CALLBACK_URL']}")

def check_actual_configuration():
    """Check your actual system configuration"""
    print(f"\n🔍 Checking your actual system configuration...")
    
    # Your actual environment variables
    config_vars = {
        'MPESA_CONSUMER_KEY': os.environ.get('MPESA_CONSUMER_KEY'),
        'MPESA_CONSUMER_SECRET': os.environ.get('MPESA_CONSUMER_SECRET'),
        'MPESA_SHORTCODE': os.environ.get('MPESA_SHORTCODE'),
        'MPESA_PASSKEY': os.environ.get('MPESA_PASSKEY'),
        'MPESA_INITIATOR_NAME': os.environ.get('MPESA_INITIATOR_NAME'),
        'MPESA_INITIATOR_PASSWORD': os.environ.get('MPESA_INITIATOR_PASSWORD'),
        'MPESA_SECURITY_CREDENTIAL': os.environ.get('MPESA_SECURITY_CREDENTIAL'),
        'MPESA_BASE_URL': os.environ.get('MPESA_BASE_URL'),
        'MPESA_RESULT_URL': os.environ.get('MPESA_RESULT_URL'),
        'MPESA_TIMEOUT_URL': os.environ.get('MPESA_TIMEOUT_URL'),
        'MPESA_CALLBACK_URL': os.environ.get('MPESA_CALLBACK_URL')
    }
    
    print(f"📋 Your actual configuration:")
    for var_name, value in config_vars.items():
        if value:
            print(f"   {var_name}: ✅ Set ({len(value)} chars)")
        else:
            print(f"   {var_name}: ❌ Not set")
    
    # Check if all required fields are present
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

def test_b2c_with_actual_config():
    """Test B2C payment using your actual configuration"""
    print(f"\n🧪 Testing B2C with your actual configuration...")
    
    try:
        # Import the enhanced MPESA service
        from app.notifications.mpesa.services import MpesaService
        
        # Initialize the service
        print("🔧 Initializing enhanced MPESA service...")
        mpesa_service = MpesaService()
        print("✅ MPESA service initialized successfully")
        
        # Test configuration validation
        print("\n🔍 Testing configuration validation...")
        try:
            mpesa_service.validate_config()
            print("✅ Configuration validation passed")
        except ValueError as e:
            print(f"❌ Configuration error: {e}")
            return False
        
        # Test OAuth token acquisition
        print("\n🔑 Testing OAuth token acquisition...")
        try:
            token = mpesa_service.get_access_token()
            if token:
                print("✅ OAuth token acquired successfully")
                print(f"   Token: {token[:20]}...")
            else:
                print("❌ Failed to acquire OAuth token")
                return False
        except Exception as e:
            print(f"❌ OAuth token error: {e}")
            return False
        
        # Test phone number formatting
        print("\n📱 Testing phone number formatting...")
        test_phone = "0708541870"
        try:
            formatted_phone = mpesa_service.format_phone_number(test_phone)
            print(f"✅ {test_phone} → {formatted_phone}")
        except Exception as e:
            print(f"❌ Phone formatting error: {e}")
            return False
        
        # Test actual B2C payment with small amount
        print(f"\n🚀 Testing actual B2C payment with ngrok callbacks...")
        print(f"   Amount: 10 KES")
        print(f"   Phone: {test_phone} → {formatted_phone}")
        print(f"   Result URL: {os.environ['MPESA_RESULT_URL']}")
        print(f"   Timeout URL: {os.environ['MPESA_TIMEOUT_URL']}")
        
        try:
            response = mpesa_service.b2c_payment(
                phone_number=test_phone,
                amount=10,
                remarks="Test B2C Payment with Ngrok"
            )
            
            print(f"\n📊 B2C Response:")
            print(f"   Response: {response}")
            
            if 'ConversationID' in response:
                print(f"\n✅ SUCCESS! B2C payment initiated!")
                print(f"   Conversation ID: {response['ConversationID']}")
                if 'ResponseDescription' in response:
                    desc = response['ResponseDescription']
                    print(f"   Description: {desc}")
                
                print(f"\n🎉 B2C TEST SUCCESSFUL!")
                print(f"📱 Check your phone (0708541870) for the payment notification")
                print(f"📊 Monitor ngrok logs for callback results")
                print(f"🌐 Ngrok URL: {NGROK_URL}")
                
                return True
            elif 'error' in response:
                print(f"\n❌ B2C payment failed: {response['error']}")
                return False
            else:
                print(f"\n⚠️ Unexpected response: {response}")
                return False
                
        except Exception as e:
            print(f"\n❌ B2C payment error: {e}")
            return False
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_test_instructions():
    """Show instructions for monitoring the test"""
    print(f"\n📋 Test Instructions:")
    print("=" * 50)
    print(f"1. 🌐 Your ngrok tunnel is running at: {NGROK_URL}")
    print(f"2. 📱 The test will send 10 KES to phone: 0708541870")
    print(f"3. 🔔 You should receive an M-Pesa notification on your phone")
    print(f"4. 📊 Check ngrok logs for callback results")
    print(f"5. 💰 If successful, you'll receive 10 KES on your phone")
    
    print(f"\n🔍 To monitor callbacks:")
    print(f"   - Check ngrok web interface: http://localhost:4040")
    print(f"   - Monitor your Flask app logs")
    print(f"   - Check your phone for M-Pesa notification")
    
    print(f"\n⚠️  Important Notes:")
    print(f"   - This is a REAL payment of 10 KES")
    print(f"   - Make sure 0708541870 is your correct phone number")
    print(f"   - The money will be deducted from your M-Pesa business account")
    print(f"   - If you want to test with a different amount, modify the script")

def main():
    """Main test function"""
    print("🧪 B2C Test with Your Actual Configuration")
    print("=" * 50)
    
    # Check your actual configuration
    if not check_actual_configuration():
        print(f"\n❌ Cannot proceed - missing required configuration")
        print(f"💡 Please ensure all required MPESA_ environment variables are set")
        return False
    
    # Set up ngrok environment
    setup_ngrok_environment()
    
    # Test ngrok connectivity
    if not test_ngrok_connectivity():
        print(f"\n❌ Cannot proceed without ngrok connectivity")
        print(f"💡 Please ensure your ngrok tunnel is running")
        return False
    
    # Show test instructions
    show_test_instructions()
    
    # Ask for confirmation
    print(f"\n🤔 Do you want to proceed with the B2C test?")
    print(f"   This will send 10 KES to 0708541870")
    response = input("   Type 'yes' to continue: ").strip().lower()
    
    if response != 'yes':
        print(f"❌ Test cancelled by user")
        return False
    
    # Run the B2C test
    success = test_b2c_with_actual_config()
    
    # Summary
    print(f"\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    if success:
        print("✅ B2C test with your actual config SUCCESSFUL!")
        print("🎉 Your enhanced B2C system is working correctly!")
        print("📱 Check your phone for the payment notification")
        print("📊 Monitor ngrok logs for callback results")
    else:
        print("❌ B2C test with your actual config FAILED!")
        print("💡 Check the error messages above and fix the issues")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 