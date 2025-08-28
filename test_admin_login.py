#!/usr/bin/env python3
"""
Test admin login with correct credentials
"""

import requests
import json

BASE_URL = "https://kibtech.coke:5000"

def test_admin_login():
    """Test admin login with correct credentials"""
    print("🔐 Testing Admin Login with Correct Credentials")
    print("=" * 60)
    
    # Test admin login
    login_data = {
        "email": "kibtechc@gmail.com",
        "password": "Kibtechceo@2018"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/admin/login", json=login_data, timeout=10)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get('data', {}).get('token')
            print(f"✅ Login successful!")
            print(f"Token: {token[:30]}..." if token else "❌ No token in response")
            
            # Test commissions endpoint
            print("\n💰 Testing Commissions Endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            commissions_response = requests.get(f"{BASE_URL}/admin/commissions/manual", headers=headers, timeout=10)
            print(f"Commissions Status: {commissions_response.status_code}")
            
            if commissions_response.status_code == 200:
                print("✅ Commissions endpoint accessible!")
                data = commissions_response.json()
                print(f"Commissions count: {len(data.get('commissions', []))}")
            else:
                print(f"❌ Commissions endpoint failed: {commissions_response.text}")
            
            # Test users endpoint
            print("\n👥 Testing Users Endpoint...")
            users_response = requests.get(f"{BASE_URL}/admin/users", headers=headers, timeout=10)
            print(f"Users Status: {users_response.status_code}")
            
            if users_response.status_code == 200:
                print("✅ Users endpoint accessible!")
                data = users_response.json()
                print(f"Users count: {len(data.get('users', []))}")
            else:
                print(f"❌ Users endpoint failed: {users_response.text}")
                
        else:
            print(f"❌ Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    test_admin_login() 