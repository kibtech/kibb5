#!/usr/bin/env python3
"""
Test script to reproduce and debug the 500 errors on /api/orders/ and /api/mpesa/payment-status/ endpoints
"""

import requests
import json
import traceback
from app import create_app, db
from app.models import User, Order, Payment
from flask_jwt_extended import create_access_token

def test_endpoints():
    """Test the problematic endpoints to identify the exact error"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test if we can create a test user and order
            print("🔍 Testing database connections and models...")
            
            # Check if we have any users
            user_count = db.session.query(User).count()
            print(f"✅ Users in database: {user_count}")
            
            # Check if we have any orders
            order_count = db.session.query(Order).count()
            print(f"✅ Orders in database: {order_count}")
            
            # Check if we have any payments
            payment_count = db.session.query(Payment).count()
            print(f"✅ Payments in database: {payment_count}")
            
            # Test with multiple users to check authorization
            all_users = db.session.query(User).limit(3).all()
            if not all_users:
                print("❌ No users found in database - cannot test JWT endpoints")
                return
            
            print(f"✅ Found {len(all_users)} users for testing")
            
            # Get payment details
            test_payment = db.session.get(Payment, 2)
            if test_payment:
                payment_owner_id = test_payment.order.user_id
                print(f"✅ Payment ID 2 belongs to User ID: {payment_owner_id}")
                
                # Find the correct user for this payment
                payment_owner = db.session.get(User, payment_owner_id)
                if payment_owner:
                    print(f"✅ Payment owner: {payment_owner.name} (ID: {payment_owner.id})")
                else:
                    print(f"❌ Payment owner user ID {payment_owner_id} not found")
            
            # Start the test client
            with app.test_client() as client:
                
                # Test with each user
                for user in all_users:
                    print(f"\n🧪 Testing with User: {user.name} (ID: {user.id})")
                    
                    # Create JWT token for this user
                    access_token = create_access_token(identity=str(user.id))
                    headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    }
                    
                    print(f"  📋 Testing /api/orders/ endpoint...")
                    try:
                        response = client.get('/api/orders/', headers=headers)
                        print(f"  Status Code: {response.status_code}")
                        if response.status_code != 200:
                            print(f"  Response: {response.get_data(as_text=True)}")
                        else:
                            data = response.get_json()
                            print(f"  Orders count: {len(data.get('orders', []))}")
                        
                        if response.status_code == 500:
                            print("  ❌ 500 Error on /api/orders/ endpoint")
                    except Exception as e:
                        print(f"  ❌ Exception during /api/orders/ test: {str(e)}")
                        traceback.print_exc()
                    
                    print(f"  💳 Testing /api/mpesa/payment-status/2 endpoint...")
                    try:
                        response = client.get('/api/mpesa/payment-status/2', headers=headers)
                        print(f"  Status Code: {response.status_code}")
                        if response.status_code != 200:
                            print(f"  Response: {response.get_data(as_text=True)}")
                        else:
                            data = response.get_json()
                            print(f"  Payment status: {data.get('payment', {}).get('status', 'Unknown')}")
                        
                        if response.status_code == 500:
                            print("  ❌ 500 Error on /api/mpesa/payment-status/2 endpoint")
                    except Exception as e:
                        print(f"  ❌ Exception during /api/mpesa/payment-status/2 test: {str(e)}")
                        traceback.print_exc()
                
                # Test with invalid payment ID
                print(f"\n🧪 Testing with invalid payment ID (999)...")
                if all_users:
                    access_token = create_access_token(identity=str(all_users[0].id))
                    headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    }
                    
                    try:
                        response = client.get('/api/mpesa/payment-status/999', headers=headers)
                        print(f"  Status Code: {response.status_code}")
                        print(f"  Response: {response.get_data(as_text=True)}")
                        
                        if response.status_code == 500:
                            print("  ❌ 500 Error with invalid payment ID")
                    except Exception as e:
                        print(f"  ❌ Exception during invalid payment ID test: {str(e)}")
                        traceback.print_exc()
                
                # Test if Payment with ID 2 exists
                print("\n🔍 Checking if Payment ID 2 exists...")
                payment_2 = db.session.get(Payment, 2)
                if payment_2:
                    print(f"✅ Payment ID 2 exists: Order ID {payment_2.order_id}, Status: {payment_2.status}")
                    # Check if the associated order exists
                    if payment_2.order:
                        print(f"✅ Associated Order exists: ID {payment_2.order.id}, User ID: {payment_2.order.user_id}")
                    else:
                        print("❌ Associated Order is missing!")
                else:
                    print("❌ Payment ID 2 does not exist")
            
        except Exception as e:
            print(f"❌ Database connection or query error: {str(e)}")
            traceback.print_exc()

if __name__ == '__main__':
    test_endpoints()