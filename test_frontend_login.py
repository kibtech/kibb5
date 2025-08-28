#!/usr/bin/env python3
"""
Test Frontend Login
This script simulates the exact frontend login request
"""

import requests
import json

def test_frontend_login():
    """Test the frontend login by simulating the exact request"""
    print("🌐 Testing Frontend Login")
    print("=" * 30)
    
    # Test URL (same as frontend)
    login_url = "http://localhost:5000/admin/login"
    
    # Test credentials (same as frontend)
    login_data = {
        "email": "kibtechc@gmail.com",
        "password": "Kibtechceo@2018"
    }
    
    # Headers (same as frontend)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print(f"🎯 Testing URL: {login_url}")
    print(f"📧 Email: {login_data['email']}")
    print(f"🔑 Password: {login_data['password']}")
    print()
    
    try:
        # Make the request
        response = requests.post(login_url, json=login_data, headers=headers, timeout=10)
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📋 Response Headers:")
        for key, value in response.headers.items():
            print(f"   {key}: {value}")
        
        print(f"\n📄 Response Body:")
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=2))
            
            if response.status_code == 200:
                print("\n✅ SUCCESS: Login response received!")
                if 'data' in response_json and 'token' in response_json['data']:
                    print("✅ Token received!")
                    print(f"   Token: {response_json['data']['token'][:50]}...")
                else:
                    print("⚠️ No token in response")
            else:
                print(f"\n❌ FAILED: Status {response.status_code}")
                if 'error' in response_json:
                    print(f"   Error: {response_json['error']}")
                    
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_frontend_login() 