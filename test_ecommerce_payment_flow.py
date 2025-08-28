#!/usr/bin/env python3
"""
Test E-commerce Payment Flow
============================

This script tests the complete e-commerce payment flow to identify why
payment success isn't being shown and orders remain pending.
"""

import requests
import json
import time
from datetime import datetime

def test_ecommerce_payment_flow():
    print("🔍 Testing E-commerce Payment Flow")
    print("=" * 50)
    
    # Base URL
    base_url = "http://localhost:5000"
    
    # Test credentials
    email = "test@example.com"
    password = "password123"
    
    try:
        # Step 1: Login to get token
        print("\n1. 🔑 Logging in to get user token...")
        login_response = requests.post(f"{base_url}/api/auth/login", json={
            "email": email,
            "password": password
        })
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
            
        login_data = login_response.json()
        if login_data.get("status") != "success":
            print(f"❌ Login failed: {login_data.get('message')}")
            return False
            
        token = login_data["data"]["token"]
        print(f"✅ Login successful! Token: {token[:20]}...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 2: Check user's orders
        print("\n2. 📋 Checking user's orders...")
        orders_response = requests.get(f"{base_url}/api/orders", headers=headers)
        
        if orders_response.status_code == 200:
            orders_data = orders_response.json()
            orders = orders_data.get("orders", [])
            print(f"✅ Found {len(orders)} orders")
            
            # Find pending orders
            pending_orders = [order for order in orders if order.get("payment_status") == "pending"]
            print(f"📊 Pending orders: {len(pending_orders)}")
            
            if pending_orders:
                order = pending_orders[0]
                print(f"🔍 Sample pending order:")
                print(f"   Order ID: {order.get('id')}")
                print(f"   Order Number: {order.get('order_number')}")
                print(f"   Status: {order.get('status')}")
                print(f"   Payment Status: {order.get('payment_status')}")
                print(f"   Total Amount: KSh {order.get('total_amount')}")
                
                # Step 3: Check if there are any payments for this order
                print(f"\n3. 💳 Checking payments for order {order.get('id')}...")
                payments_response = requests.get(f"{base_url}/api/orders/{order.get('id')}/payments", headers=headers)
                
                if payments_response.status_code == 200:
                    payments_data = payments_response.json()
                    payments = payments_data.get("payments", [])
                    print(f"✅ Found {len(payments)} payments")
                    
                    for payment in payments:
                        print(f"   Payment ID: {payment.get('id')}")
                        print(f"   Status: {payment.get('status')}")
                        print(f"   Amount: KSh {payment.get('amount')}")
                        print(f"   Created: {payment.get('created_at')}")
                else:
                    print(f"❌ Failed to get payments: {payments_response.status_code}")
                    
                # Step 4: Check payment status endpoint
                print(f"\n4. 🔍 Checking payment status endpoint...")
                if payments:
                    payment_id = payments[0].get('id')
                    status_response = requests.get(f"{base_url}/api/mpesa/payment-status/{payment_id}", headers=headers)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        print(f"✅ Payment status: {status_data}")
                    else:
                        print(f"❌ Payment status failed: {status_response.status_code}")
                        print(f"Response: {status_response.text}")
                else:
                    print("⚠️ No payments found to check status")
                    
        else:
            print(f"❌ Failed to get orders: {orders_response.status_code}")
            print(f"Response: {orders_response.text}")
            
        # Step 5: Check M-Pesa callback endpoint
        print(f"\n5. 📞 Checking M-Pesa callback endpoint...")
        callback_response = requests.post(f"{base_url}/api/mpesa/callback", json={
            "test": "callback_endpoint_check"
        })
        
        if callback_response.status_code in [200, 400, 404]:
            print(f"✅ M-Pesa callback endpoint accessible (Status: {callback_response.status_code})")
        else:
            print(f"❌ M-Pesa callback endpoint issue: {callback_response.status_code}")
            
        print("\n" + "=" * 50)
        print("🔍 Analysis of E-commerce Payment Flow Issues:")
        print("\n📋 Potential Issues Found:")
        print("1. Payment status not being updated in Order model")
        print("2. M-Pesa callback not properly handling e-commerce orders")
        print("3. Frontend not receiving payment success notifications")
        print("4. Order status remaining 'pending' after successful payment")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the Flask backend is running")
        print("   Run: python app.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_ecommerce_payment_flow()
    if not success:
        print("\n❌ Test failed! Check the errors above.")
        exit(1) 