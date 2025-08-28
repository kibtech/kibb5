#!/usr/bin/env python3
"""
Test script to verify wallet PIN integration
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api/wallet"

def test_pin_integration():
    """Test the complete PIN integration flow"""
    
    print("🔐 Testing Wallet PIN Integration")
    print("=" * 50)
    
    # You'll need to get a valid JWT token first
    # This is a placeholder - you'll need to login and get the token
    auth_token = "YOUR_JWT_TOKEN_HERE"  # Replace with actual token
    
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test 1: Check PIN status
        print("\n1. Testing PIN Status Check...")
        response = requests.get(f"{API_BASE}/pin/status", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            pin_status = response.json()
            print(f"   Has PIN: {pin_status.get('has_wallet_pin')}")
            print(f"   Can Withdraw: {pin_status.get('can_withdraw')}")
            print(f"   Message: {pin_status.get('message')}")
        else:
            print(f"   Error: {response.text}")
        
        # Test 2: Set PIN (if not already set)
        print("\n2. Testing PIN Setup...")
        pin_data = {
            "pin": "1234",
            "confirm_pin": "1234"
        }
        response = requests.post(f"{API_BASE}/pin/set", headers=headers, json=pin_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ PIN set successfully")
        elif response.status_code == 400:
            result = response.json()
            if "already set" in result.get('error', '').lower():
                print("   ℹ️  PIN already set")
            else:
                print(f"   ❌ Error: {result.get('error')}")
        else:
            print(f"   ❌ Error: {response.text}")
        
        # Test 3: Verify PIN
        print("\n3. Testing PIN Verification...")
        verify_data = {"pin": "1234"}
        response = requests.post(f"{API_BASE}/pin/verify", headers=headers, json=verify_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ PIN verified: {result.get('verified')}")
        else:
            print(f"   ❌ Error: {response.text}")
        
        # Test 4: Test withdrawal with PIN
        print("\n4. Testing Withdrawal with PIN...")
        withdrawal_data = {
            "amount": 10,
            "phone_number": "254712345678",
            "pin": "1234"
        }
        response = requests.post(f"{API_BASE}/withdrawals", headers=headers, json=withdrawal_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Withdrawal request created successfully")
        elif response.status_code == 400:
            result = response.json()
            if "insufficient" in result.get('error', '').lower():
                print("   ℹ️  Insufficient balance (expected)")
            elif "pin_required" in result.get('error', '').lower():
                print("   ℹ️  PIN required (expected)")
            else:
                print(f"   ❌ Error: {result.get('error')}")
        else:
            print(f"   ❌ Error: {response.text}")
        
        # Test 5: Test withdrawal without PIN (should fail)
        print("\n5. Testing Withdrawal without PIN...")
        withdrawal_data_no_pin = {
            "amount": 10,
            "phone_number": "254712345678"
        }
        response = requests.post(f"{API_BASE}/withdrawals", headers=headers, json=withdrawal_data_no_pin)
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            result = response.json()
            if "pin" in result.get('error', '').lower():
                print("   ✅ Correctly rejected withdrawal without PIN")
            else:
                print(f"   ❌ Unexpected error: {result.get('error')}")
        else:
            print(f"   ❌ Should have been rejected: {response.text}")
        
        print("\n🎉 PIN Integration Test Completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def test_frontend_endpoints():
    """Test that all required endpoints exist"""
    
    print("\n🔍 Testing Frontend Endpoints")
    print("=" * 50)
    
    endpoints = [
        "/api/wallet/pin/status",
        "/api/wallet/pin/set", 
        "/api/wallet/pin/change",
        "/api/wallet/pin/verify",
        "/api/wallet/withdrawals"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.options(f"{BASE_URL}{endpoint}")
            print(f"✅ {endpoint} - {response.status_code}")
        except:
            print(f"❌ {endpoint} - Connection failed")

if __name__ == "__main__":
    print("Wallet PIN Integration Test")
    print("Make sure your Flask server is running on http://localhost:5000")
    print("You'll need to update the auth_token in the script with a valid JWT token")
    print()
    
    test_frontend_endpoints()
    test_pin_integration() 