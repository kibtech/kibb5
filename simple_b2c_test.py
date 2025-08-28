#!/usr/bin/env python3
"""
Simple B2C Test Script
======================

A quick test to verify if M-Pesa B2C withdrawal is working.
This script will attempt to send a small amount to test the B2C integration.
"""

import os
import sys
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_b2c_withdrawal():
    """Test B2C withdrawal functionality"""
    
    print("=" * 50)
    print("   SIMPLE B2C WITHDRAWAL TEST")
    print("=" * 50)
    
    try:
        # Import Flask app and M-Pesa service only
        from app import create_app
        from app.notifications.mpesa.services import MpesaService
        
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            print("\n🔍 Step 1: Checking M-Pesa configuration...")
            
            # Check if M-Pesa is configured
            required_configs = [
                'MPESA_CONSUMER_KEY',
                'MPESA_CONSUMER_SECRET', 
                'MPESA_SHORTCODE',
                'MPESA_BASE_URL',
                'MPESA_INITIATOR_NAME',
                'MPESA_INITIATOR_PASSWORD'
            ]
            
            missing_configs = []
            for config in required_configs:
                if not app.config.get(config):
                    missing_configs.append(config)
            
            if missing_configs:
                print(f"❌ Missing M-Pesa configurations: {', '.join(missing_configs)}")
                print("   Please check your environment variables or config.py")
                return False
            
            print("✅ M-Pesa configuration found")
            
            # Use the provided phone number
            test_phone = "254708541870"  # Convert to international format
            test_amount = 10  # 10 KSh test amount
            
            print(f"\n🚀 Step 2: Testing B2C payment...")
            print(f"   - Phone: {test_phone}")
            print(f"   - Amount: KSh {test_amount}")
            
            # Initialize M-Pesa service
            mpesa_service = MpesaService()
            
            # Test access token first
            print("\n🔑 Step 3: Getting access token...")
            try:
                access_token = mpesa_service.get_access_token()
                print(f"✅ Access token obtained: {access_token[:20]}...")
            except Exception as e:
                print(f"❌ Failed to get access token: {e}")
                return False
            
            # Test B2C payment
            print(f"\n💸 Step 4: Initiating B2C payment...")
            print(f"   - Sending KSh {test_amount} to {test_phone}")
            
            b2c_response = mpesa_service.b2c_payment(
                phone_number=test_phone,
                amount=test_amount,
                remarks="B2C Test Payment"
            )
            
            print(f"\n📊 B2C Response:")
            print(f"   - Response: {b2c_response}")
            
            if 'ConversationID' in b2c_response:
                print(f"\n✅ B2C payment initiated successfully!")
                print(f"   - Conversation ID: {b2c_response['ConversationID']}")
                print(f"   - Originator Conversation ID: {b2c_response.get('OriginatorConversationID', 'N/A')}")
                
                if 'ResponseDescription' in b2c_response:
                    desc = b2c_response['ResponseDescription']
                    print(f"   - Description: {desc}")
                
                print(f"\n🎉 B2C TEST SUCCESSFUL!")
                print(f"   - The payment request was sent to M-Pesa")
                print(f"   - Check your phone for any M-Pesa notifications")
                print(f"   - The actual transfer will depend on your M-Pesa account balance")
                
            elif 'error' in b2c_response:
                print(f"\n❌ B2C payment failed: {b2c_response['error']}")
                print(f"   - Check your M-Pesa configuration")
                print(f"   - Verify your initiator credentials")
                print(f"   - Ensure your account has sufficient balance")
                
            else:
                print(f"\n⚠️ Unexpected B2C response: {b2c_response}")
                print(f"   - This might indicate a configuration issue")
            
            print(f"\n📋 Summary:")
            print(f"   1. M-Pesa configuration: ✅")
            print(f"   2. Access token: ✅")
            print(f"   3. B2C request sent: {'✅' if 'ConversationID' in b2c_response else '❌'}")
            
            if 'ConversationID' in b2c_response:
                print(f"\n✅ B2C withdrawal test completed successfully!")
                print(f"   - Your B2C integration is working")
                print(f"   - Check your M-Pesa account for the transaction")
            else:
                print(f"\n❌ B2C withdrawal test failed")
                print(f"   - Check the error message above")
                print(f"   - Verify your M-Pesa configuration")
            
            return 'ConversationID' in b2c_response
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_b2c_withdrawal()
    if success:
        print(f"\n🎯 B2C test completed successfully!")
    else:
        print(f"\n💥 B2C test failed!")
    
    input("\nPress Enter to exit...") 