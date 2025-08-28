import requests
import json

def test_auth_endpoints():
    """Test the authentication endpoints after fixes"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Authentication Endpoints")
    print("=" * 40)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server is not responding properly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on http://localhost:5000")
        return
    
    # Test 2: Test registration
    print("\n📝 Testing User Registration...")
    register_data = {
        "name": "Test User",
        "phone": "254700000001",
        "email": "testuser@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/register", json=register_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
        else:
            print("❌ Registration failed!")
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test 3: Test login
    print("\n🔐 Testing User Login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            if 'access_token' in data:
                print(f"✅ JWT token received: {data['access_token'][:20]}...")
        else:
            print("❌ Login failed!")
            
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Test 4: Test login with non-existent user
    print("\n🔐 Testing Login with Non-existent User...")
    fake_login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=fake_login_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ Correctly rejected invalid credentials!")
        else:
            print("❌ Unexpected response for invalid credentials!")
            
    except Exception as e:
        print(f"❌ Error testing invalid login: {e}")

if __name__ == "__main__":
    test_auth_endpoints() 