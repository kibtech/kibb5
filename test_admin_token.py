#!/usr/bin/env python3
"""
Test Admin Token Authentication
"""

import requests
import json

def test_admin_token():
    """Test admin token authentication"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Admin Token Authentication")
    print("=" * 50)
    
    # Test 1: Try to access protected endpoint without token
    print("\n1. 🔒 Testing protected endpoint WITHOUT token...")
    try:
        response = requests.get(f"{base_url}/admin/profile")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Login to get token
    print("\n2. 🔑 Logging in to get admin token...")
    try:
        login_data = {
            "email": "kibtechc@gmail.com",
            "password": "Kibtechceo@2018"
        }
        
        response = requests.post(f"{base_url}/admin/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                token = data['data']['token']
                print(f"   ✅ Login successful!")
                print(f"   Token: {token[:20]}...")
                
                # Test 3: Access protected endpoint WITH token
                print("\n3. 🔓 Testing protected endpoint WITH token...")
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                
                # Test profile endpoint
                profile_response = requests.get(f"{base_url}/admin/profile", headers=headers)
                print(f"   Profile Status: {profile_response.status_code}")
                if profile_response.status_code == 200:
                    print(f"   ✅ Profile access successful!")
                else:
                    print(f"   ❌ Profile access failed: {profile_response.json()}")
                
                # Test commissions endpoint
                commissions_response = requests.get(f"{base_url}/admin/commissions", headers=headers)
                print(f"   Commissions Status: {commissions_response.status_code}")
                if commissions_response.status_code == 200:
                    print(f"   ✅ Commissions access successful!")
                    data = commissions_response.json()
                    print(f"   Commission Count: {len(data.get('commissions', []))}")
                else:
                    print(f"   ❌ Commissions access failed: {commissions_response.json()}")
                
                # Test analytics endpoint
                analytics_response = requests.get(f"{base_url}/admin/commissions/analytics", headers=headers)
                print(f"   Analytics Status: {analytics_response.status_code}")
                if analytics_response.status_code == 200:
                    print(f"   ✅ Analytics access successful!")
                else:
                    print(f"   ❌ Analytics access failed: {analytics_response.json()}")
                
            else:
                print(f"   ❌ Login failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ Login request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error during login: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Token authentication test completed!")

if __name__ == "__main__":
    test_admin_token() 