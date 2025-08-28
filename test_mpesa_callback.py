#!/usr/bin/env python3
"""
Test MPesa Callback System
This script tests the MPesa callback endpoint to identify why payments
aren't being completed after successful STK Push.
"""

import os
import sys
import requests
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import CyberServiceOrder, User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mpesa_callback():
    """Test the MPesa callback system"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 TESTING MPESA CALLBACK SYSTEM")
        print("=" * 50)
        
        # Check the recent order that's stuck
        order_number = "CS2025081320430924"
        order = CyberServiceOrder.query.filter_by(order_number=order_number).first()
        
        if not order:
            print(f"❌ Order {order_number} not found")
            return
        
        print(f"📦 Order Details:")
        print(f"   Order Number: {order.order_number}")
        print(f"   Status: {order.status}")
        print(f"   Payment Status: {order.payment_status}")
        print(f"   Amount: KSh {order.amount}")
        print(f"   User: {order.user.email if order.user else 'Unknown'}")
        print(f"   Created: {order.created_at}")
        
        # Check if user was referred
        if order.user and order.user.referred_by_id:
            referrer = User.query.get(order.user.referred_by_id)
            print(f"   Referred by: {referrer.email if referrer else 'Unknown'}")
            print(f"   Referral Code: {order.user.referral_code}")
        else:
            print(f"   Referred by: No referral relationship")
        
        print(f"\n🔧 CALLBACK SYSTEM STATUS:")
        
        # Check callback URL configuration
        from flask import current_app
        callback_url = current_app.config.get('MPESA_CALLBACK_URL')
        print(f"   Callback URL: {callback_url}")
        
        # Check if callback URL is accessible
        try:
            response = requests.get(callback_url, timeout=10)
            print(f"   Callback URL Accessible: ✅ (Status: {response.status_code})")
        except Exception as e:
            print(f"   Callback URL Accessible: ❌ ({str(e)})")
        
        # Check if there are any pending payments with this checkout request ID
        print(f"\n💰 PAYMENT STATUS:")
        print(f"   Current Status: {order.status}")
        print(f"   Payment Status: {order.payment_status}")
        
        if order.payment_status == 'pending':
            print(f"   ⚠️  Payment is still pending - callback not received")
        elif order.payment_status == 'paid':
            print(f"   ✅ Payment completed successfully")
        else:
            print(f"   ❓ Unknown payment status: {order.payment_status}")
        
        # Check if commission was processed
        from app.models import Commission
        commission = Commission.query.filter_by(order_id=order.id).first()
        
        if commission:
            print(f"   💰 Commission: ✅ KSh {commission.amount} processed")
        else:
            print(f"   💰 Commission: ❌ Not processed yet")
        
        print(f"\n🔍 DIAGNOSIS:")
        
        if order.payment_status == 'pending':
            print(f"   ❌ PAYMENT STUCK: MPesa callback not received")
            print(f"   💡 Possible causes:")
            print(f"      1. Callback URL not accessible from Safaricom servers")
            print(f"      2. Network/firewall blocking the callback")
            print(f"      3. Callback endpoint processing failing")
            print(f"      4. MPesa service not sending callback")
        else:
            print(f"   ✅ Payment appears to be working")
        
        print(f"\n🛠️  RECOMMENDED ACTIONS:")
        print(f"   1. Check if your server is accessible from the internet")
        print(f"   2. Verify callback URL is publicly accessible")
        print(f"   3. Check server logs for callback errors")
        print(f"   4. Test callback endpoint manually")
        print(f"   5. Contact Safaricom support if callbacks aren't being sent")

def test_callback_endpoint():
    """Test the callback endpoint manually"""
    
    print(f"\n🧪 MANUAL CALLBACK TEST:")
    print(f"   To test if your callback endpoint works, you can:")
    print(f"   1. Use a tool like ngrok to expose your local server")
    print(f"   2. Update your MPesa callback URL to the ngrok URL")
    print(f"   3. Make a test payment to see if callback is received")
    print(f"   4. Check server logs for callback processing")

if __name__ == "__main__":
    try:
        test_mpesa_callback()
        test_callback_endpoint()
        
    except Exception as e:
        logger.error(f"Failed to test MPesa callback: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 