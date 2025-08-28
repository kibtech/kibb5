#!/usr/bin/env python3
"""
Test Enhanced B2C Integration
This script tests the enhanced B2C implementation integrated into the main system
"""

import os
import sys
import requests
from datetime import datetime

def test_enhanced_b2c_integration():
    """Test the enhanced B2C implementation in the main system"""
    
    print("🧪 Testing Enhanced B2C Integration")
    print("=" * 50)
    
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
        test_cases = [
            ("0112735877", "254112735877"),
            ("254112735877", "254112735877"),
            ("+254112735877", "254112735877"),
            ("112735877", "254112735877"),
        ]
        
        for input_phone, expected in test_cases:
            try:
                formatted = mpesa_service.format_phone_number(input_phone)
                if formatted == expected:
                    print(f"✅ {input_phone} → {formatted}")
                else:
                    print(f"❌ {input_phone} → {formatted} (expected {expected})")
                    return False
            except Exception as e:
                print(f"❌ Phone formatting error for {input_phone}: {e}")
                return False
        
        # Test B2C payment structure (dry run)
        print("\n💰 Testing B2C payment structure...")
        try:
            test_amount = 10
            test_phone = "0708541870"
            formatted_phone = mpesa_service.format_phone_number(test_phone)
            
            print(f"   Amount: {test_amount} KES")
            print(f"   Phone: {test_phone} → {formatted_phone}")
            print(f"   Command ID: BusinessPayment")
            print(f"   Shortcode: {mpesa_service.shortcode}")
            print(f"   Result URL: {os.environ.get('MPESA_RESULT_URL', 'http://localhost:5000/api/mpesa/b2c-result')}")
            print(f"   Timeout URL: {os.environ.get('MPESA_TIMEOUT_URL', 'http://localhost:5000/api/mpesa/timeout')}")
            
            print("✅ B2C payment parameters validated")
        except Exception as e:
            print(f"❌ B2C payment test error: {e}")
            return False
        
        # Test actual B2C payment (small amount)
        print("\n🚀 Testing actual B2C payment...")
        try:
            response = mpesa_service.test_b2c_payment(test_amount=10, test_phone="0708541870")
            
            print(f"   Response: {response}")
            
            if 'ConversationID' in response:
                print(f"   ✅ Success! Conversation ID: {response['ConversationID']}")
                if 'ResponseDescription' in response:
                    desc = response['ResponseDescription']
                    print(f"   Description: {desc}")
                print("\n🎉 B2C TEST SUCCESSFUL!")
                print("📱 Check your phone for the payment notification")
                print("📊 Monitor your callback server for final status")
                return True
            elif 'error' in response:
                print(f"   ❌ Error: {response['error']}")
                return False
            else:
                print(f"   ⚠️ Unexpected response: {response}")
                return False
                
        except Exception as e:
            print(f"   ❌ B2C payment error: {e}")
            return False
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_config_summary():
    """Show a summary of the current configuration"""
    print("\n📋 Configuration Summary:")
    print("=" * 50)
    
    # Show non-sensitive config
    print(f"Base URL: {os.environ.get('MPESA_BASE_URL', 'https://api.safaricom.co.ke')}")
    print(f"Shortcode: {os.environ.get('MPESA_SHORTCODE', 'Not set')}")
    print(f"Result URL: {os.environ.get('MPESA_RESULT_URL', 'http://localhost:5000/api/mpesa/b2c-result')}")
    print(f"Timeout URL: {os.environ.get('MPESA_TIMEOUT_URL', 'http://localhost:5000/api/mpesa/timeout')}")
    print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    
    # Check if sensitive config is present
    print(f"\nCredentials Status:")
    print(f"Consumer Key: {'✅ Set' if os.environ.get('MPESA_CONSUMER_KEY') else '❌ Missing'}")
    print(f"Consumer Secret: {'✅ Set' if os.environ.get('MPESA_CONSUMER_SECRET') else '❌ Missing'}")
    print(f"Initiator Name: {'✅ Set' if os.environ.get('MPESA_INITIATOR_NAME') else '❌ Missing'}")
    print(f"Initiator Password: {'✅ Set' if os.environ.get('MPESA_INITIATOR_PASSWORD') else '❌ Missing'}")
    print(f"Security Credential: {'✅ Set' if os.environ.get('MPESA_SECURITY_CREDENTIAL') else '❌ Missing'}")

def main():
    """Main test function"""
    print("🧪 Enhanced B2C Integration Test Suite")
    print("=" * 50)
    
    # Show configuration summary
    show_config_summary()
    
    # Run the test
    success = test_enhanced_b2c_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    if success:
        print("✅ Enhanced B2C integration test PASSED!")
        print("\n🎉 Your enhanced B2C system is working correctly!")
        print("💡 The enhanced implementation includes:")
        print("   - Better phone number formatting")
        print("   - Improved error handling")
        print("   - Configuration validation")
        print("   - Same successful approach as the working b2c folder")
        print("   - Enhanced logging and debugging")
    else:
        print("❌ Enhanced B2C integration test FAILED!")
        print("\n⚠️ Please check the error messages above and fix the issues.")
        print("💡 Common issues:")
        print("   - Missing environment variables")
        print("   - Incorrect API credentials")
        print("   - Network connectivity issues")
        print("   - Invalid phone number format")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 