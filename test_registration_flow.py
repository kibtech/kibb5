#!/usr/bin/env python3
import requests
import json

# Base URL
BASE_URL = 'http://localhost:5000'

def test_registration_flow():
    """Test the complete registration flow"""
    
    # Test registration
    print("1. Testing registration...")
    register_data = {
        'name': 'Test User',
        'phone': '254700000000',
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    register_response = requests.post(f'{BASE_URL}/api/auth/register', json=register_data)
    print(f"Registration status: {register_response.status_code}")
    print(f"Registration response: {register_response.text}")
    
    if register_response.status_code != 201:
        print("❌ Registration failed")
        return
    
    # Test login with unverified email
    print("\n2. Testing login with unverified email...")
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    login_response = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
    print(f"Login status: {login_response.status_code}")
    print(f"Login response: {login_response.text}")
    
    # Test resend verification
    print("\n3. Testing resend verification...")
    resend_data = {
        'email': 'test@example.com'
    }
    
    resend_response = requests.post(f'{BASE_URL}/api/auth/resend-verification', json=resend_data)
    print(f"Resend verification status: {resend_response.status_code}")
    print(f"Resend verification response: {resend_response.text}")

if __name__ == '__main__':
    test_registration_flow() 