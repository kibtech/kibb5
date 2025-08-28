#!/usr/bin/env python3
"""
Final B2C Test - 10 KES Withdrawal
==================================
Final attempt to get B2C working for 10 KES withdrawal.
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
import subprocess

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup_google_dns():
    """Setup requests to use Google DNS"""
    print("🔧 Setting up Google DNS...")
    
    # Create a session with custom DNS resolution
    session = requests.Session()
    
    # Override the default resolver to use Google DNS
    def google_dns_resolver(hostname):
        """Resolve hostname using Google DNS"""
        try:
            # Use nslookup with Google DNS
            result = subprocess.run(
                ['nslookup', hostname, '8.8.8.8'], 
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                # Parse the output to get the IP
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Address:' in line and not line.startswith('Server:'):
                        ip = line.split('Address:')[-1].strip()
                        if ip and ip != '8.8.8.8':
                            print(f"   ✅ Resolved {hostname} -> {ip} via Google DNS")
                            return ip
            
            # Fallback to direct IP if known
            if hostname == 'api.safaricom.co.ke':
                return '196.201.214.202'
                
        except Exception as e:
            print(f"   ❌ DNS resolution failed: {e}")
        
        return None
    
    # Monkey patch the session to use our resolver
    original_get = session.get
    original_post = session.post
    
    def custom_get(url, *args, **kwargs):
        """Custom GET with DNS resolution"""
        if 'api.safaricom.co.ke' in url:
            ip = google_dns_resolver('api.safaricom.co.ke')
            if ip:
                # Replace hostname with IP in URL
                url = url.replace('api.safaricom.co.ke', ip)
                # Add Host header to maintain the original hostname
                if 'headers' not in kwargs:
                    kwargs['headers'] = {}
                kwargs['headers']['Host'] = 'api.safaricom.co.ke'
                # Disable SSL verification when using IP address
                kwargs['verify'] = False
        
        return original_get(url, *args, **kwargs)
    
    def custom_post(url, *args, **kwargs):
        """Custom POST with DNS resolution"""
        if 'api.safaricom.co.ke' in url:
            ip = google_dns_resolver('api.safaricom.co.ke')
            if ip:
                # Replace hostname with IP in URL
                url = url.replace('api.safaricom.co.ke', ip)
                # Add Host header to maintain the original hostname
                if 'headers' not in kwargs:
                    kwargs['headers'] = {}
                kwargs['headers']['Host'] = 'api.safaricom.co.ke'
                # Disable SSL verification when using IP address
                kwargs['verify'] = False
        
        return original_post(url, *args, **kwargs)
    
    session.get = custom_get
    session.post = custom_post
    
    return session

def test_b2c_final():
    """Final B2C test with 10 KES"""
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Final B2C Test - 10 KES Withdrawal")
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
        
        # Check if user has enough balance
        test_amount = 10
        if wallet.balance < test_amount:
            print(f"\n❌ Insufficient balance for KSh {test_amount} withdrawal")
            print(f"   Current balance: KSh {wallet.balance}")
            print(f"   Required: KSh {test_amount}")
            print(f"   Need to add: KSh {test_amount - wallet.balance}")
            return
        
        # Setup Google DNS
        session = setup_google_dns()
        
        # Test M-Pesa service
        print(f"\n🧪 Testing B2C Service:")
        
        try:
            # Create MpesaService and override its session
            mpesa_service = MpesaService()
            
            # Override the requests session with Google DNS
            mpesa_service.session = session
            
            # Test access token
            print("   - Getting access token...")
            access_token = mpesa_service.get_access_token()
            
            if access_token and isinstance(access_token, str):
                print("   ✅ Access token obtained successfully")
                print(f"   - Token: {access_token[:20]}...")
            else:
                print(f"   ❌ Failed to get access token: {access_token}")
                return
            
            # Test B2C payment with 10 KES
            test_phone = "254712591937"  # User's specified phone number with country code
            
            print(f"   - Testing B2C payment of KSh {test_amount} to {test_phone}...")
            print(f"   💰 This should send money TO your phone (not ask you to pay)")
            
            b2c_response = mpesa_service.b2c_payment(
                phone_number=test_phone,
                amount=test_amount,
                remarks=f"Withdrawal of KSh {test_amount} for {user.name}"
            )
            
            print(f"   - B2C Response: {b2c_response}")
            
            if 'ConversationID' in b2c_response:
                print("   ✅ B2C payment initiated successfully!")
                print(f"   - Conversation ID: {b2c_response['ConversationID']}")
                print(f"   - Originator Conversation ID: {b2c_response.get('OriginatorConversationID', 'N/A')}")
                
                # Check if OTP is required
                if 'ResponseDescription' in b2c_response:
                    desc = b2c_response['ResponseDescription']
                    if 'otp' in desc.lower() or 'passcode' in desc.lower():
                        print(f"   🔐 OTP Required: {desc}")
                        print(f"   📱 Check your phone for SMS with OTP")
                        print(f"   💡 You need to complete this in M-Pesa business portal")
                        print(f"   📞 Contact Safaricom (100) to disable OTP requirement")
                    else:
                        print(f"   🎉 No OTP required! Money should be sent automatically!")
                
            elif 'error' in b2c_response:
                print(f"   ❌ B2C payment failed: {b2c_response['error']}")
            else:
                print(f"   ⚠️ Unexpected B2C response: {b2c_response}")
                
        except Exception as e:
            print(f"   ❌ Error testing M-Pesa service: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print(f"\n💡 B2C vs STK Push Explanation:")
        print("=" * 40)
        print("B2C (Business to Customer):")
        print("   ✅ Business SENDS money to customer")
        print("   ✅ Customer RECEIVES money")
        print("   ✅ Used for withdrawals")
        print("   ❌ Requires OTP in your case")
        
        print(f"\nSTK Push (Customer to Business):")
        print("   ❌ Customer PAYS money to business")
        print("   ❌ Customer SENDS money")
        print("   ❌ Used for payments/deposits")
        print("   ✅ Works without OTP")
        
        print(f"\n🔧 To Fix B2C OTP Issue:")
        print("   1. Contact Safaricom Business Support (100)")
        print("   2. Ask to disable OTP requirement for B2C")
        print("   3. Verify your business account is fully activated")
        print("   4. Request proper security credential format")
        
        print(f"\n✅ Final B2C test completed!")

if __name__ == "__main__":
    test_b2c_final() 