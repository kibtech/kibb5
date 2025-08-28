#!/usr/bin/env python3
"""
Test B2C Withdrawal with OTP Handling
=====================================
Test the M-Pesa B2C withdrawal functionality with OTP support.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal
from app.mpesa.services import MpesaService
from decimal import Decimal
import requests
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_b2c_with_otp():
    """Test B2C withdrawal with OTP handling"""
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Testing B2C Withdrawal with OTP Support")
        print("=" * 60)
        
        # Find the test user
        user = User.query.filter_by(email='kashdyke@gmail.com').first()
        if not user:
            print("❌ User not found")
            return
        
        wallet = user.wallet
        if not wallet:
            print("❌ Wallet not found")
            return
        
        print(f"👤 User: {user.name} ({user.email})")
        print(f"📱 Phone: {user.phone}")
        print(f"💰 Current balances:")
        print(f"   - Total Balance: KSh {wallet.balance}")
        print(f"   - Deposited Balance: KSh {wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {wallet.commission_balance}")
        print(f"   - Withdrawable Balance: KSh {wallet.get_withdrawable_amount()}")
        
        # Test M-Pesa service
        print(f"\n🧪 Testing M-Pesa Service:")
        
        try:
            mpesa_service = MpesaService()
            
            # Test access token
            print("   - Getting access token...")
            access_token = mpesa_service.get_access_token()
            
            if access_token and isinstance(access_token, str):
                print("   ✅ Access token obtained successfully")
                print(f"   - Token: {access_token[:20]}...")
            else:
                print(f"   ❌ Failed to get access token: {access_token}")
                return
            
            # Test B2C payment with user's specified number and amount
            test_amount = 1  # Small amount for testing
            test_phone = "254712591937"  # User's specified phone number with country code
            
            print(f"   - Testing B2C payment of KSh {test_amount} to {test_phone}...")
            print(f"   ⚠️  You may receive an SMS with OTP")
            
            b2c_response = mpesa_service.b2c_payment(
                phone_number=test_phone,
                amount=test_amount,
                remarks=f"Test withdrawal with OTP for {user.name}"
            )
            
            print(f"   - B2C Response: {b2c_response}")
            
            if 'ConversationID' in b2c_response:
                print("   ✅ B2C payment initiated successfully!")
                print(f"   - Conversation ID: {b2c_response['ConversationID']}")
                print(f"   - Originator Conversation ID: {b2c_response.get('OriginatorConversationID', 'N/A')}")
                
                # Check if OTP is required
                if 'ResponseDescription' in b2c_response:
                    desc = b2c_response['ResponseDescription']
                    if 'otp' in desc.lower() or 'passcode' in desc.lower() or 'code' in desc.lower():
                        print(f"   🔐 OTP Required: {desc}")
                        print(f"   📱 Check your phone for SMS with OTP")
                        
                        # Ask user for OTP
                        otp = input("   🔢 Enter the OTP from SMS (or press Enter to skip): ").strip()
                        
                        if otp:
                            print(f"   🔐 Submitting OTP: {otp}")
                            # Here you would submit the OTP to complete the transaction
                            # This requires additional API calls to M-Pesa
                            print(f"   ⚠️  OTP submission not yet implemented")
                            print(f"   💡 You may need to complete this manually in M-Pesa portal")
                        else:
                            print(f"   ⏭️  Skipping OTP submission")
                
            elif 'error' in b2c_response:
                print(f"   ❌ B2C payment failed: {b2c_response['error']}")
            else:
                print(f"   ⚠️ Unexpected B2C response: {b2c_response}")
                
        except Exception as e:
            print(f"   ❌ Error testing M-Pesa service: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print(f"\n💡 OTP Process Information:")
        print(f"   1. M-Pesa sends OTP via SMS for security")
        print(f"   2. OTP is required to complete B2C transactions")
        print(f"   3. You can complete manually in M-Pesa business portal")
        print(f"   4. Or implement OTP handling in your application")
        
        print(f"\n🔧 Manual Completion Steps:")
        print(f"   1. Go to M-Pesa business portal")
        print(f"   2. Find pending B2C transaction")
        print(f"   3. Enter OTP: 855756 (from your SMS)")
        print(f"   4. Complete the transaction")
        
        print(f"\n✅ B2C withdrawal test completed!")

if __name__ == "__main__":
    test_b2c_with_otp() 