#!/usr/bin/env python3
import requests
import json

BASE_URL = 'https://kibtech.coke:5000'

def test_admin_session():
    """Test admin session maintenance"""
    print("1. Testing admin login...")
    
    login_data = {
        'email': 'kibtechc@gmail.com',
        'password': 'Kibtechceo@2018'
    }
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # Test admin login
        login_response = session.post(f'{BASE_URL}/admin/login', json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ Login successful!")
            print(f"Session cookies: {dict(session.cookies)}")
            
            # Test check-auth endpoint
            print("\n2. Testing check-auth endpoint...")
            check_response = session.get(f'{BASE_URL}/admin/check-auth')
            print(f"Check-auth status: {check_response.status_code}")
            
            if check_response.status_code == 200:
                print("✅ Authentication check successful!")
                
                # Test admin profile endpoint
                print("\n3. Testing admin profile endpoint...")
                profile_response = session.get(f'{BASE_URL}/admin/profile')
                print(f"Profile status: {profile_response.status_code}")
                
                if profile_response.status_code == 200:
                    print("✅ Profile access successful!")
                else:
                    print(f"❌ Profile access failed: {profile_response.text}")
                    
                # Test admin analytics endpoint
                print("\n4. Testing admin analytics endpoint...")
                analytics_response = session.get(f'{BASE_URL}/admin/analytics/comprehensive-dashboard?days=7')
                print(f"Analytics status: {analytics_response.status_code}")
                
                if analytics_response.status_code == 200:
                    print("✅ Analytics access successful!")
                else:
                    print(f"❌ Analytics access failed: {analytics_response.text}")
                    
            else:
                print("❌ Authentication check failed!")
                print(f"Response: {check_response.text}")
                
        else:
            print("❌ Login failed!")
            print(f"Response: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_admin_session() 