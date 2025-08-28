#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_complete_payment_flow():
    """Test the complete payment flow including status checking"""
    print("1. Testing login to get JWT token...")
    login_data = {
        'email': 'kashdyke@gmail.com',
        'password': '2128557353'
    }
    
    try:
        login_response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            response_data = login_response.json()
            token = response_data.get('access_token')
            
            if token:
                print(f"Token received: {token[:50]}...")
                headers = {'Authorization': f'Bearer {token}'}
                
                # Create a test order
                print("\n2. Creating a test order...")
                order_data = {
                    'items': [
                        {
                            'product_id': 1,
                            'quantity': 1,
                            'price': 1000.00
                        }
                    ],
                    'phone_number': '254712591937',
                    'total_amount': 1000.00
                }
                
                order_response = requests.post(f'{BASE_URL}/api/orders/create', headers=headers, json=order_data)
                print(f"Order creation status: {order_response.status_code}")
                
                if order_response.status_code == 201:
                    order_data = order_response.json()
                    order_id = order_data['order']['id']
                    print(f"Order created with ID: {order_id}")
                    
                    # Test STK push
                    print("\n3. Testing STK push...")
                    stk_data = {
                        'order_id': order_id,
                        'phone_number': '254712591937'
                    }
                    
                    stk_response = requests.post(f'{BASE_URL}/api/mpesa/stk-push', headers=headers, json=stk_data)
                    print(f"STK push status: {stk_response.status_code}")
                    print(f"STK push response: {stk_response.text}")
                    
                    if stk_response.status_code == 200:
                        payment_data = stk_response.json()
                        payment_id = payment_data.get('payment_id')
                        
                        if payment_id:
                            print(f"\n4. Testing payment status checking...")
                            print(f"Payment ID: {payment_id}")
                            
                            # Check payment status a few times
                            for i in range(5):
                                print(f"Checking payment status (attempt {i+1})...")
                                status_response = requests.get(f'{BASE_URL}/api/mpesa/payment-status/{payment_id}', headers=headers)
                                print(f"Status response: {status_response.status_code}")
                                
                                if status_response.status_code == 200:
                                    status_data = status_response.json()
                                    payment_status = status_data['payment']['status']
                                    print(f"Payment status: {payment_status}")
                                    
                                    if payment_status == 'completed':
                                        print("✅ Payment completed successfully!")
                                        break
                                    elif payment_status == 'failed':
                                        print("❌ Payment failed")
                                        break
                                
                                time.sleep(2)  # Wait 2 seconds between checks
                        else:
                            print("❌ No payment ID received")
                    else:
                        print(f"❌ STK push failed: {stk_response.text}")
                else:
                    print(f"❌ Order creation failed: {order_response.text}")
            else:
                print("❌ No token received")
        else:
            print("❌ Login failed")
            print(f"Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_complete_payment_flow() 