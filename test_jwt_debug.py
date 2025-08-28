#!/usr/bin/env python3
import requests
import json
import jwt
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5000'

def test_jwt_debug():
    """Test JWT token creation and validation"""
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
                
                # Try to decode the token manually
                try:
                    # Note: This will fail without the secret key, but we can see the structure
                    decoded = jwt.decode(token, options={"verify_signature": False})
                    print(f"Token payload: {json.dumps(decoded, indent=2)}")
                except Exception as e:
                    print(f"Token decode error: {e}")
                
                print("\n2. Testing profile endpoint with token...")
                headers = {'Authorization': f'Bearer {token}'}
                profile_response = requests.get(f'{BASE_URL}/api/auth/profile', headers=headers)
                print(f"Profile status: {profile_response.status_code}")
                print(f"Profile response: {profile_response.text}")
                
                if profile_response.status_code == 200:
                    print("✅ Profile request successful")
                else:
                    print("❌ Profile request failed")
                    
                    # Test without Bearer prefix
                    print("\n3. Testing profile endpoint without Bearer prefix...")
                    headers_no_bearer = {'Authorization': token}
                    profile_response2 = requests.get(f'{BASE_URL}/api/auth/profile', headers=headers_no_bearer)
                    print(f"Profile status (no Bearer): {profile_response2.status_code}")
                    print(f"Profile response (no Bearer): {profile_response2.text}")
                    
            else:
                print("❌ No token received")
        else:
            print("❌ Login failed")
            print(f"Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_jwt_debug() 