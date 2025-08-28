#!/usr/bin/env python3
"""
Immediate CORS Test
This script will test CORS immediately after server restart
"""

import requests
import time
import json

def test_cors_immediate():
    """Test CORS immediately after server start"""
    print("🚀 Testing CORS Configuration Immediately...")
    print("=" * 50)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test OPTIONS request (preflight)
        print("🔍 Testing OPTIONS request...")
        response = requests.options(
            'http://localhost:5000/admin/login',
            headers={
                'Origin': 'http://127.0.0.1:5000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            },
            timeout=5
        )
        
        print(f"OPTIONS Status: {response.status_code}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
        
        if response.status_code == 200:
            print("✅ OPTIONS request successful!")
        else:
            print("❌ OPTIONS request failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("Make sure the server is running: python run.py")
        return
        
    # Test actual login request
    print("\n🔐 Testing login request...")
    try:
        response = requests.post(
            'http://localhost:5000/admin/login',
            json={
                "email": "kibtechc@gmail.com",
                "password": "Kibtechceo@2018"
            },
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login request successful!")
            print("✅ CORS is working properly!")
            
            data = response.json()
            print(f"Admin: {data['data']['admin']['first_name']} {data['data']['admin']['last_name']}")
            print(f"Token: {data['data']['token'][:20]}...")
            
            print("\n🎯 Next Steps:")
            print("1. Open your browser")
            print("2. Go to: http://localhost:5000/admin")
            print("3. Login with: kibtechc@gmail.com / Kibtechceo@2018")
            
        else:
            print("❌ Login request failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_cors_immediate() 