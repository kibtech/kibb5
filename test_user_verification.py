#!/usr/bin/env python3
import requests
import json

# Base URL
BASE_URL = 'http://localhost:5000'

def test_user_verification():
    """Test user verification status and login flow"""
    
    # Test with a known unverified email
    test_email = 'test@example.com'
    
    print(f"Testing with email: {test_email}")
    
    # First, let's try to register a new user
    print("\n1. Testing registration...")
    register_data = {
        'name': 'Test User',
        'phone': '254700000000',
        'email': test_email,
        'password': 'password123'
    }
    
    register_response = requests.post(f'{BASE_URL}/api/auth/register', json=register_data)
    print(f"Registration status: {register_response.status_code}")
    print(f"Registration response: {register_response.text}")
    
    # Now try to login with unverified email
    print("\n2. Testing login with unverified email...")
    login_data = {
        'email': test_email,
        'password': 'password123'
    }
    
    login_response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
    print(f"Login status: {login_response.status_code}")
    print(f"Login response: {login_response.text}")
    
    # Check if we got a 403 (should happen for unverified email)
    if login_response.status_code == 403:
        print("✅ Correctly blocked unverified email login")
        response_data = login_response.json()
        if response_data.get('needs_verification'):
            print("✅ Correctly identified needs verification")
        else:
            print("❌ Missing needs_verification flag")
    else:
        print(f"❌ Expected 403, got {login_response.status_code}")

if __name__ == '__main__':
    test_user_verification() 