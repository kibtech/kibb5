#!/usr/bin/env python3
"""
Test CORS Fix
This script will test if the CORS configuration is working properly
"""

import requests
import json

def test_cors():
    """Test CORS configuration"""
    print("🌐 Testing CORS Configuration...")
    print("=" * 40)
    
    # Test OPTIONS request (preflight)
    try:
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
            print("✅ CORS preflight successful!")
        else:
            print("❌ CORS preflight failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("Make sure your Flask server is running:")
        print("python run.py")
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
            
            print("\n🎯 Next Steps:")
            print("1. Open your browser")
            print("2. Go to: http://localhost:5000/admin")
            print("3. Login with:")
            print("   Email: kibtechc@gmail.com")
            print("   Password: Kibtechceo@2018")
            
        else:
            print("❌ Login request failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_cors() 