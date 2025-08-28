#!/usr/bin/env python3
"""
Test B2C Withdrawal with KIBTECH Initiator
==========================================
Test B2C withdrawal using the new KIBTECH initiator name.
"""

import os
import sys
import subprocess
import requests
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import User, Wallet, Withdrawal
from app.mpesa.services import MpesaService

def setup_google_dns():
    """Setup Google DNS resolution to bypass local DNS issues"""
    class GoogleDNSSession(requests.Session):
        def request(self, method, url, **kwargs):
            # Resolve hostname using Google DNS
            if 'api.safaricom.co.ke' in url:
                try:
                    result = subprocess.run(
                        ['nslookup', 'api.safaricom.co.ke', '8.8.8.8'],
                        capture_output=True, text=True, timeout=10
                    )
                    
                    if result.returncode == 0:
                        # Extract IP from nslookup output
                        for line in result.stdout.split('\n'):
                            if 'Address:' in line and '8.8.8.8' not in line:
                                ip = line.split('Address:')[-1].strip()
                                if ip and ip != '8.8.8.8':
                                    # Replace hostname with IP
                                    url = url.replace('api.safaricom.co.ke', ip)
                                    # Disable SSL verification for IP
                                    kwargs['verify'] = False
                                    break
                except Exception as e:
                    print(f"⚠️  DNS resolution failed: {e}")
            
            return super().request(method, url, **kwargs)
    
    return GoogleDNSSession()

def test_b2c_with_kibtech_initiator():
    """Test B2C withdrawal with KIBTECH initiator"""
    
    print("🚀 Testing B2C Withdrawal with KIBTECH Initiator")
    print("=" * 60)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Get test user
        user = User.query.filter_by(email='kashdyke@gmail.com').first()
        if not user:
            print("❌ Test user not found")
            return
        
        # Get user's wallet
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        if not wallet:
            print("❌ User wallet not found")
            return
        
        print(f"👤 User: {user.name} ({user.email})")
        print(f"📱 Phone: {user.phone}")
        print(f"💰 Current balances:")
        print(f"   - Total Balance: KSh {wallet.balance:.2f}")
        print(f"   - Deposited Balance: KSh {wallet.deposited_balance:.2f}")
        print(f"   - Commission Balance: KSh {wallet.commission_balance:.2f}")
        print(f"   - Withdrawable Balance: KSh {wallet.get_withdrawable_amount():.2f}")
        
        # Check if user has sufficient balance
        test_amount = 5
        if wallet.get_withdrawable_amount() < test_amount:
            print(f"❌ Insufficient balance for withdrawal. Need KSh {test_amount}, have KSh {wallet.get_withdrawable_amount():.2f}")
            return
        
        print(f"\n🔧 Setting up Google DNS...")
        
        # Setup M-Pesa service with Google DNS
        mpesa_service = MpesaService()
        mpesa_service.session = setup_google_dns()
        
        print(f"🧪 Testing M-Pesa Service (with KIBTECH initiator):")
        
        # Test access token
        print(f"   - Getting access token...")
        try:
            access_token = mpesa_service.get_access_token()
            if access_token:
                print(f"   ✅ Access token obtained successfully")
                print(f"   - Token: {access_token[:20]}...")
            else:
                print(f"   ❌ Failed to get access token")
                return
        except Exception as e:
            print(f"   ❌ Error getting access token: {e}")
            return
        
        # Test B2C payment
        test_phone = "254712591937"  # Your test phone number
        print(f"   - Testing B2C payment of KSh {test_amount} to {test_phone}...")
        print(f"   💰 This should send money TO your phone (not ask you to pay)")
        
        try:
            result = mpesa_service.b2c_payment(test_phone, test_amount, "Test withdrawal with KIBTECH initiator")
            
            if result.get('ResponseCode') == '0':
                print(f"   ✅ B2C payment initiated successfully!")
                print(f"   - Conversation ID: {result.get('ConversationID')}")
                print(f"   - Originator Conversation ID: {result.get('OriginatorConversationID')}")
                
                # Check if OTP is required
                if 'OTP' in str(result) or 'otp' in str(result).lower():
                    print(f"   📱 OTP required - check your phone for SMS")
                else:
                    print(f"   ✅ No OTP required - payment should process automatically")
                    
            else:
                print(f"   ❌ B2C payment failed: {result}")
                
        except Exception as e:
            print(f"   ❌ Error during B2C payment: {e}")
        
        print(f"\n🧪 Testing Withdrawal Endpoint:")
        print(f"   - Testing withdrawal of KSh {test_amount} to {test_phone}...")
        
        # Test withdrawal endpoint
        try:
            # Validate withdrawal amount
            if test_amount <= 0:
                print(f"   ❌ Invalid withdrawal amount")
                return
            
            if test_amount > wallet.get_withdrawable_amount():
                print(f"   ❌ Insufficient balance for withdrawal")
                return
            
            print(f"   ✅ Withdrawal amount is valid")
            
            # Deduct from wallet using the proper method
            if not wallet.deduct_withdrawal(test_amount):
                print(f"   ❌ Failed to deduct from wallet")
                return
            
            # Create withdrawal record
            withdrawal = Withdrawal(
                user_id=user.id,
                amount=test_amount,
                phone_number=test_phone,
                status='pending'
            )
            
            from app import db
            db.session.add(withdrawal)
            db.session.commit()
            
            print(f"   ✅ Amount deducted from wallet")
            
            # Attempt B2C payment
            result = mpesa_service.b2c_payment(test_phone, test_amount, f"Withdrawal for user {user.name}")
            
            if result.get('ResponseCode') == '0':
                print(f"   ✅ Withdrawal initiated successfully!")
                print(f"   - Withdrawal ID: {withdrawal.id}")
                print(f"   - Conversation ID: {result.get('ConversationID')}")
                
                # Update withdrawal status
                withdrawal.status = 'processing'
                withdrawal.conversation_id = result.get('ConversationID')
                withdrawal.transaction_id = result.get('OriginatorConversationID')
                db.session.commit()
                
            else:
                print(f"   ❌ B2C payment failed: {result}")
                # Revert wallet deduction - add back the amount
                wallet.add_deposit(test_amount)
                withdrawal.status = 'failed'
                db.session.commit()
                
        except Exception as e:
            print(f"   ❌ Error during withdrawal: {e}")
            # Revert wallet deduction on error
            try:
                wallet.add_deposit(test_amount)
                db.session.commit()
            except:
                pass
        
        print(f"\n✅ B2C withdrawal test completed!")
        print(f"📱 Check your phone ({test_phone}) for the money transfer")

if __name__ == "__main__":
    test_b2c_with_kibtech_initiator() 