#!/usr/bin/env python3
"""
Simple Admin Login Test
This script will test the admin login and provide clear instructions
"""

import requests
import json

def test_admin_login():
    """Test admin login and provide instructions"""
    print("🔐 Testing Admin Login...")
    print("=" * 40)
    
    # Admin credentials
    credentials = {
        "email": "kibtechc@gmail.com",
        "password": "Kibtechceo@2018"
    }
    
    try:
        # Test login
        response = requests.post(
            'http://localhost:5000/admin/login',
            json=credentials,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LOGIN SUCCESSFUL!")
            print(f"Admin: {data['data']['admin']['first_name']} {data['data']['admin']['last_name']}")
            print(f"Email: {data['data']['admin']['email']}")
            print(f"Role: {data['data']['admin']['role']['name']}")
            print(f"Token: {data['data']['token'][:20]}...")
            
            print("\n🎯 LOGIN INSTRUCTIONS:")
            print("1. Open your browser")
            print("2. Go to: http://localhost:5000/admin")
            print("3. Use these credentials:")
            print(f"   Email: {credentials['email']}")
            print(f"   Password: {credentials['password']}")
            print("4. Click Login")
            
            print("\n✅ Your admin login should work now!")
            
        else:
            print("❌ Login failed!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("Make sure your Flask server is running:")
        print("python app.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_admin_login() 