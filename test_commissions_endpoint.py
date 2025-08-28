#!/usr/bin/env python3
"""
Test Commissions Endpoint Directly
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_commissions_endpoint():
    """Test commissions endpoint directly"""
    print("🔍 Testing Commissions Endpoint Directly")
    print("=" * 50)
    
    # Step 1: Login to get token
    print("\n1. 🔐 Logging in...")
    login_data = {
        "email": "kibtechc@gmail.com",
        "password": "Kibtechceo@2018"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/admin/login", json=login_data, timeout=10)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.text}")
            return
        
        login_data = login_response.json()
        token = login_data.get('data', {}).get('token')
        print(f"✅ Login successful! Token: {token[:30]}..." if token else "❌ No token")
        
        if not token:
            print("❌ No token received")
            return
        
        # Step 2: Test commissions endpoint
        print("\n2. 💰 Testing Commissions Endpoint...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print(f"Headers being sent: {headers}")
        
        commissions_response = requests.get(f"{BASE_URL}/admin/commissions/manual", headers=headers, timeout=10)
        print(f"Commissions Status: {commissions_response.status_code}")
        print(f"Commissions Response: {commissions_response.text}")
        
        if commissions_response.status_code == 200:
            print("✅ Commissions endpoint working!")
            data = commissions_response.json()
            print(f"Commissions count: {len(data.get('commissions', []))}")
        else:
            print(f"❌ Commissions endpoint failed")
            
        # Step 3: Test users endpoint for comparison
        print("\n3. 👥 Testing Users Endpoint...")
        users_response = requests.get(f"{BASE_URL}/admin/users", headers=headers, timeout=10)
        print(f"Users Status: {users_response.status_code}")
        
        if users_response.status_code == 200:
            print("✅ Users endpoint working!")
            data = users_response.json()
            print(f"Users count: {len(data.get('users', []))}")
        else:
            print(f"❌ Users endpoint failed: {users_response.text}")
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    test_commissions_endpoint() 