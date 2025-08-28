#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_payment_flow():
    """Test the complete payment flow to debug the 403 error"""
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
                
                # First, let's check the user's profile to see their ID
                print("\n2. Checking user profile...")
                profile_response = requests.get(f'{BASE_URL}/api/auth/profile', headers=headers)
                print(f"Profile status: {profile_response.status_code}")
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    user_id = profile_data['user']['id']
                    print(f"User ID: {user_id} (type: {type(user_id)})")
                
                # Now let's create a test order
                print("\n3. Creating a test order...")
                order_data = {
                    'items': [
                        {
                            'product_id': 1,  # Assuming product ID 1 exists
                            'quantity': 1,
                            'price': 1000.00  # Adding price for the item
                        }
                    ],
                    'phone_number': '254712591937',  # Phone number for order
                    'total_amount': 1000.00  # Total amount for the order
                }
                
                order_response = requests.post(f'{BASE_URL}/api/orders/create', headers=headers, json=order_data)
                print(f"Order creation status: {order_response.status_code}")
                
                if order_response.status_code == 201:
                    order_data = order_response.json()
                    order_id = order_data['order']['id']
                    print(f"Order created with ID: {order_id}")
                    
                    # Now test the STK push
                    print("\n4. Testing STK push...")
                    stk_data = {
                        'order_id': order_id,
                        'phone_number': '254712591937'  # Using the provided phone number
                    }
                    
                    stk_response = requests.post(f'{BASE_URL}/api/mpesa/stk-push', headers=headers, json=stk_data)
                    print(f"STK push status: {stk_response.status_code}")
                    print(f"STK push response: {stk_response.text}")
                    
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
    test_payment_flow() 