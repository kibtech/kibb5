import requests
import json

# Test the login API
def test_login():
    # Test data
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        # Test login
        response = requests.post('http://localhost:5000/api/auth/login', json=login_data)
        print(f"Login Response Status: {response.status_code}")
        print(f"Login Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Access Token: {data.get('access_token', 'No token')}")
            print(f"User: {data.get('user', 'No user data')}")
        else:
            print("❌ Login failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_register():
    # Test registration
    register_data = {
        "name": "Test User 2",
        "phone": "254700000001",
        "email": "test2@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post('http://localhost:5000/api/auth/register', json=register_data)
        print(f"\nRegister Response Status: {response.status_code}")
        print(f"Register Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
        else:
            print("❌ Registration failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("Testing KibTech Login System...")
    print("=" * 40)
    
    test_login()
    test_register() 