#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_dashboard_endpoints():
    """Test dashboard endpoints"""
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
                
                print("\n2. Testing /api/wallet/stats...")
                wallet_response = requests.get(f'{BASE_URL}/api/wallet/stats', headers=headers)
                print(f"Wallet stats status: {wallet_response.status_code}")
                print(f"Wallet stats response: {wallet_response.text}")
                
                print("\n3. Testing /api/auth/referral-stats...")
                referral_response = requests.get(f'{BASE_URL}/api/auth/referral-stats', headers=headers)
                print(f"Referral stats status: {referral_response.status_code}")
                print(f"Referral stats response: {referral_response.text}")
                
            else:
                print("❌ No token received")
        else:
            print("❌ Login failed")
            print(f"Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_dashboard_endpoints() 