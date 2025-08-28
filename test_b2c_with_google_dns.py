#!/usr/bin/env python3
"""
Test B2C Withdrawal with Google DNS Fix
======================================
Test the M-Pesa B2C withdrawal functionality using Google DNS to bypass local DNS issues.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal
from app.mpesa.services import MpesaService
from decimal import Decimal
import requests
import socket
import urllib3

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
            import subprocess
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

def test_b2c_withdrawal():
    """Test B2C withdrawal functionality with DNS fix"""
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Testing B2C Withdrawal (with Google DNS fix)")
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
        
        # Setup Google DNS
        session = setup_google_dns()
        
        # Test M-Pesa service with DNS fix
        print(f"\n🧪 Testing M-Pesa Service (with DNS fix):")
        
        try:
            # Create a custom MpesaService that uses our session
            mpesa_service = MpesaService()
            
            # Override the requests session
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
            
            # Test B2C payment with user's specified number and amount
            test_amount = 5  # 5 KES as requested
            test_phone = "254708541870"  # User's specified phone number with country code
            
            print(f"   - Testing B2C payment of KSh {test_amount} to {test_phone}...")
            
            b2c_response = mpesa_service.b2c_payment(
                phone_number=test_phone,
                amount=test_amount,
                remarks=f"Test withdrawal for {user.name}"
            )
            
            print(f"   - B2C Response: {b2c_response}")
            
            if 'ConversationID' in b2c_response:
                print("   ✅ B2C payment initiated successfully!")
                print(f"   - Conversation ID: {b2c_response['ConversationID']}")
                print(f"   - Originator Conversation ID: {b2c_response.get('OriginatorConversationID', 'N/A')}")
            elif 'error' in b2c_response:
                print(f"   ❌ B2C payment failed: {b2c_response['error']}")
            else:
                print(f"   ⚠️ Unexpected B2C response: {b2c_response}")
                
        except Exception as e:
            print(f"   ❌ Error testing M-Pesa service: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Test withdrawal endpoint
        print(f"\n🧪 Testing Withdrawal Endpoint:")
        
        try:
            from app.mpesa.routes import initiate_withdrawal
            from flask import request, jsonify
            from flask_jwt_extended import create_access_token
            
            # Create test data with user's specified values
            test_data = {
                'amount': 5,  # 5 KES as requested
                'phone_number': "254712591937"  # User's specified phone number with country code
            }
            
            print(f"   - Testing withdrawal of KSh {test_data['amount']} to {test_data['phone_number']}...")
            
            # This would normally be called via HTTP request
            # For testing, we'll simulate the logic
            if wallet.can_withdraw(test_data['amount']):
                print("   ✅ Withdrawal amount is valid")
                
                # Create withdrawal record
                withdrawal = Withdrawal(
                    user_id=user.id,
                    amount=test_data['amount'],
                    phone_number=test_data['phone_number'],
                    status='pending'
                )
                db.session.add(withdrawal)
                db.session.flush()
                
                # Deduct from wallet
                if wallet.deduct_withdrawal(test_data['amount']):
                    print("   ✅ Amount deducted from wallet")
                    
                    # Initiate B2C payment with DNS fix
                    b2c_response = mpesa_service.b2c_payment(
                        phone_number=test_data['phone_number'],
                        amount=float(test_data['amount']),
                        remarks=f"Withdrawal for user {user.name}"
                    )
                    
                    if 'ConversationID' in b2c_response:
                        withdrawal.conversation_id = b2c_response['ConversationID']
                        db.session.commit()
                        print("   ✅ Withdrawal initiated successfully!")
                        print(f"   - Withdrawal ID: {withdrawal.id}")
                        print(f"   - Conversation ID: {withdrawal.conversation_id}")
                    else:
                        db.session.rollback()
                        print(f"   ❌ B2C payment failed: {b2c_response}")
                else:
                    db.session.rollback()
                    print("   ❌ Failed to deduct amount from wallet")
            else:
                print("   ❌ Insufficient balance for withdrawal")
                
        except Exception as e:
            print(f"   ❌ Error testing withdrawal endpoint: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print(f"\n✅ B2C withdrawal test completed!")

if __name__ == "__main__":
    test_b2c_withdrawal() 