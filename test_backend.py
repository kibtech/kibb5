#!/usr/bin/env python3
"""
Test Backend Connection and Login
"""

import requests
import json

def test_backend():
    """Test backend connection and login"""
    print("🔍 Testing KIBTECH Backend...")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test 1: Check if backend is running
        print("1. Testing backend connection...")
        response = requests.get(f"{base_url}/api/products/featured?limit=1", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
        
        # Test 2: Try admin login
        print("\n2. Testing admin login...")
        admin_data = {
            "email": "kibtechc@gmail.com",
            "password": "admin123"
        }
        
        response = requests.post(f"{base_url}/api/auth/login", json=admin_data, timeout=5)
        print(f"Admin login status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Admin login successful!")
            data = response.json()
            print(f"Token: {data.get('token', 'No token')[:20]}...")
        else:
            print(f"❌ Admin login failed: {response.text}")
        
        # Test 3: Try user login
        print("\n3. Testing user login...")
        user_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        
        response = requests.post(f"{base_url}/api/auth/login", json=user_data, timeout=5)
        print(f"User login status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ User login successful!")
            data = response.json()
            print(f"Token: {data.get('token', 'No token')[:20]}...")
        else:
            print(f"❌ User login failed: {response.text}")
        
        # Test 4: Check what users exist
        print("\n4. Checking available users...")
        response = requests.get(f"{base_url}/api/auth/users", timeout=5)
        if response.status_code == 200:
            users = response.json()
            print(f"Found {len(users)} users")
            for user in users:
                print(f"  - {user.get('email')} (Verified: {user.get('email_verified')})")
        else:
            print(f"Could not get users: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        print("💡 Start the backend with: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def main():
    """Main function"""
    if test_backend():
        print("\n🎉 Backend test completed!")
        print("\n📋 If login is still failing:")
        print("1. Check if users exist in database")
        print("2. Ensure email verification is disabled")
        print("3. Try creating a new user account")
    else:
        print("\n❌ Backend test failed!")
        print("Please start the backend server first")

if __name__ == '__main__':
    main() 