#!/usr/bin/env python3
"""
Test STK Push for Withdrawals (Alternative to B2C)
==================================================
Use STK Push as an alternative to B2C for withdrawals.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet
from app.mpesa.services import MpesaService
from decimal import Decimal
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_stk_withdrawal():
    """Test STK Push for withdrawals"""
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Testing STK Push for Withdrawals")
        print("=" * 50)
        
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
        
        # Test STK Push for withdrawal
        print(f"\n🧪 Testing STK Push for Withdrawal:")
        
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
            
            # Test STK Push for withdrawal
            test_amount = 1  # Small amount for testing
            test_phone = "254712591937"  # User's specified phone number
            
            print(f"   - Testing STK Push of KSh {test_amount} to {test_phone}...")
            print(f"   📱 User will receive STK Push on their phone")
            
            stk_response = mpesa_service.stk_push(
                phone_number=test_phone,
                amount=test_amount,
                account_reference="Withdrawal",
                transaction_desc=f"Withdrawal for {user.name}"
            )
            
            print(f"   - STK Push Response: {stk_response}")
            
            if 'CheckoutRequestID' in stk_response:
                print("   ✅ STK Push initiated successfully!")
                print(f"   - CheckoutRequestID: {stk_response['CheckoutRequestID']}")
                print(f"   - MerchantRequestID: {stk_response.get('MerchantRequestID', 'N/A')}")
                print(f"   - ResponseCode: {stk_response.get('ResponseCode', 'N/A')}")
                print(f"   - ResponseDescription: {stk_response.get('ResponseDescription', 'N/A')}")
                
                print(f"\n📱 Next Steps:")
                print(f"   1. Check phone {test_phone} for STK Push")
                print(f"   2. Enter M-Pesa PIN when prompted")
                print(f"   3. Confirm the transaction")
                print(f"   4. Money will be sent to the phone")
                
            elif 'error' in stk_response:
                print(f"   ❌ STK Push failed: {stk_response['error']}")
            else:
                print(f"   ⚠️ Unexpected STK Push response: {stk_response}")
                
        except Exception as e:
            print(f"   ❌ Error testing STK Push: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print(f"\n💡 STK Push vs B2C Comparison:")
        print("=" * 40)
        print("STK Push (Customer Initiated):")
        print("   ✅ Works reliably")
        print("   ✅ No OTP issues")
        print("   ✅ User confirms on phone")
        print("   ❌ Requires user interaction")
        print("   ❌ User needs to enter PIN")
        
        print(f"\nB2C (Business Initiated):")
        print("   ❌ OTP issues in your case")
        print("   ❌ Business account configuration problems")
        print("   ✅ Fully automated")
        print("   ✅ No user interaction required")
        
        print(f"\n✅ STK Push withdrawal test completed!")

if __name__ == "__main__":
    test_stk_withdrawal() 