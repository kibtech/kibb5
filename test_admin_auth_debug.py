#!/usr/bin/env python3
"""
Test script to debug admin authentication issues
"""

import requests
import json

BASE_URL = "https://kibtech.coke:5000"

def test_admin_auth():
    """Test admin authentication flow"""
    print("🔍 Testing Admin Authentication Debug")
    print("=" * 50)
    
    # Step 1: Test admin login
    print("\n1. 🔐 Testing Admin Login...")
    login_data = {
        "email": "kibtechc@gmail.com",
        "password": "Kibtechceo@2018"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/admin/login", json=login_data, timeout=10)
        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get('data', {}).get('token')
            print(f"✅ Login successful! Token: {token[:20]}..." if token else "❌ No token in response")
            
            # Step 2: Test profile endpoint with token
            print("\n2. 👤 Testing Profile Endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            profile_response = requests.get(f"{BASE_URL}/admin/profile", headers=headers, timeout=10)
            print(f"Profile Status: {profile_response.status_code}")
            print(f"Profile Response: {profile_response.text}")
            
            # Step 3: Test commissions endpoint with token
            print("\n3. 💰 Testing Commissions Endpoint...")
            commissions_response = requests.get(f"{BASE_URL}/admin/commissions/manual", headers=headers, timeout=10)
            print(f"Commissions Status: {commissions_response.status_code}")
            print(f"Commissions Response: {commissions_response.text}")
            
            # Step 4: Test users endpoint with token
            print("\n4. 👥 Testing Users Endpoint...")
            users_response = requests.get(f"{BASE_URL}/admin/users", headers=headers, timeout=10)
            print(f"Users Status: {users_response.status_code}")
            print(f"Users Response: {users_response.text}")
            
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    test_admin_auth() 