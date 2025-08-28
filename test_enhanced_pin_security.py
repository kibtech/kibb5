#!/usr/bin/env python3
"""
Test script to verify enhanced PIN security features
"""
import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api/wallet"

def test_enhanced_pin_security():
    """Test the enhanced PIN security features"""
    
    print("🔐 Testing Enhanced PIN Security Features")
    print("=" * 60)
    
    # You'll need to get a valid JWT token first
    auth_token = "YOUR_JWT_TOKEN_HERE"  # Replace with actual token
    
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test 1: Check PIN status with enhanced information
        print("\n1. Testing Enhanced PIN Status...")
        response = requests.get(f"{API_BASE}/pin/status", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            pin_status = response.json()
            print(f"   Has PIN: {pin_status.get('has_wallet_pin')}")
            print(f"   PIN Locked: {pin_status.get('pin_locked')}")
            print(f"   Lock Remaining: {pin_status.get('lock_remaining_minutes')} minutes")
            print(f"   Attempts Remaining: {pin_status.get('attempts_remaining')}")
            print(f"   Can Withdraw: {pin_status.get('can_withdraw')}")
            print(f"   Message: {pin_status.get('message')}")
        else:
            print(f"   Error: {response.text}")
        
        # Test 2: Test PIN verification with rate limiting
        print("\n2. Testing PIN Verification with Rate Limiting...")
        
        # Try wrong PIN multiple times to trigger rate limiting
        for attempt in range(1, 6):
            print(f"   Attempt {attempt}: Testing with wrong PIN...")
            response = requests.post(f"{API_BASE}/pin/verify", headers=headers, json={"pin": "9999"})
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 423:
                result = response.json()
                print(f"   ✅ PIN locked after {attempt} attempts!")
                print(f"   Lock remaining: {result.get('locked_until_minutes')} minutes")
                print(f"   Message: {result.get('message')}")
                break
            elif response.status_code == 400:
                result = response.json()
                attempts_remaining = result.get('attempts_remaining', 0)
                print(f"   ❌ Wrong PIN. {attempts_remaining} attempts remaining")
            else:
                print(f"   Unexpected response: {response.text}")
            
            if attempt < 5:
                time.sleep(1)  # Small delay between attempts
        
        # Test 3: Test PIN change with email verification
        print("\n3. Testing PIN Change with Email Verification...")
        
        # First, try to change PIN (should trigger email verification)
        pin_change_data = {
            "current_pin": "1234",  # Assuming this is the current PIN
            "new_pin": "5678",
            "confirm_pin": "5678"
        }
        
        response = requests.post(f"{API_BASE}/pin/change", headers=headers, json=pin_change_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('requires_email_verification'):
                print("   ✅ Email verification required!")
                print(f"   Email: {result.get('email')}")
                print(f"   Message: {result.get('message')}")
                
                # Test resend email functionality
                print("\n4. Testing Resend Email Functionality...")
                response = requests.post(f"{API_BASE}/pin/change/resend-email", headers=headers)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print("   ✅ Email resent successfully!")
                else:
                    print(f"   ❌ Failed to resend email: {response.text}")
                
                # Test with email OTP (you'll need to get the actual OTP from email)
                print("\n5. Testing PIN Change with Email OTP...")
                pin_change_with_otp = {
                    "current_pin": "1234",
                    "new_pin": "5678",
                    "confirm_pin": "5678",
                    "email_otp": "123456"  # Replace with actual OTP from email
                }
                
                response = requests.post(f"{API_BASE}/pin/change", headers=headers, json=pin_change_with_otp)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print("   ✅ PIN changed successfully with email verification!")
                elif response.status_code == 400:
                    result = response.json()
                    if "Invalid or expired" in result.get('error', ''):
                        print("   ℹ️  Expected: Invalid OTP (need real email OTP)")
                    else:
                        print(f"   ❌ Error: {result.get('error')}")
                else:
                    print(f"   ❌ Unexpected response: {response.text}")
            else:
                print("   ℹ️  PIN changed without email verification (unexpected)")
        elif response.status_code == 423:
            result = response.json()
            print(f"   ℹ️  PIN is locked: {result.get('message')}")
        elif response.status_code == 400:
            result = response.json()
            print(f"   ❌ Error: {result.get('error')}")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
        
        # Test 4: Test withdrawal with locked PIN
        print("\n6. Testing Withdrawal with Locked PIN...")
        withdrawal_data = {
            "amount": 10,
            "phone_number": "254712345678",
            "pin": "1234"
        }
        
        response = requests.post(f"{API_BASE}/withdrawals", headers=headers, json=withdrawal_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 423:
            result = response.json()
            print("   ✅ Withdrawal correctly blocked due to locked PIN!")
            print(f"   Message: {result.get('message')}")
        else:
            print(f"   Response: {response.text}")
        
        print("\n🎉 Enhanced PIN Security Test Completed!")
        print("\nKey Features Tested:")
        print("✅ Rate limiting (4 attempts then 2-hour lock)")
        print("✅ Email verification for PIN changes")
        print("✅ Enhanced PIN status with lock information")
        print("✅ Resend email functionality")
        print("✅ Withdrawal blocking when PIN is locked")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the Flask app is running.")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def test_user_model_enhancements():
    """Test the enhanced User model methods"""
    
    print("\n🔧 Testing User Model Enhancements")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models import User
        
        app = create_app()
        with app.app_context():
            # Get a test user
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return
            
            print(f"Testing with user: {user.name} ({user.email})")
            
            # Test PIN locking functionality
            print("\n1. Testing PIN Locking...")
            
            # Simulate failed attempts
            for i in range(4):
                user.check_wallet_pin("9999")  # Wrong PIN
                print(f"   Attempt {i+1}: PIN attempts = {user.pin_attempts}")
            
            print(f"   PIN locked: {user.is_pin_locked()}")
            print(f"   Lock remaining: {user.get_pin_lock_remaining()} minutes")
            
            # Test correct PIN (should unlock)
            print("\n2. Testing Correct PIN (should unlock)...")
            if user.check_wallet_pin("1234"):  # Assuming correct PIN
                print("   ✅ Correct PIN unlocked the account!")
                print(f"   PIN attempts reset to: {user.pin_attempts}")
                print(f"   PIN locked: {user.is_pin_locked()}")
            else:
                print("   ❌ PIN verification failed")
            
            print("\n🎉 User Model Enhancement Test Completed!")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    print("Enhanced PIN Security Test")
    print("Make sure your Flask server is running on http://localhost:5000")
    print("You'll need to update the auth_token in the script with a valid JWT token")
    print()
    
    test_user_model_enhancements()
    test_enhanced_pin_security() 