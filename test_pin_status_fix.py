#!/usr/bin/env python3
"""
Test script to verify PIN status endpoint fix
"""
from app import create_app, db
from app.models import User

def test_pin_status():
    """Test PIN status functionality"""
    
    print("🔐 Testing PIN Status Fix")
    print("=" * 40)
    
    app = create_app()
    with app.app_context():
        try:
            # Get a test user
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return
            
            print(f"Testing with user: {user.name} ({user.email})")
            
            # Test PIN attempts remaining property
            print(f"\n1. Testing PIN Attempts Remaining...")
            print(f"   PIN attempts: {user.pin_attempts}")
            print(f"   PIN attempts remaining: {user.pin_attempts_remaining}")
            
            # Test PIN lock status
            print(f"\n2. Testing PIN Lock Status...")
            print(f"   PIN locked: {user.is_pin_locked()}")
            print(f"   Lock remaining: {user.get_pin_lock_remaining()} minutes")
            
            # Test PIN status
            print(f"\n3. Testing PIN Status...")
            print(f"   Has PIN: {user.has_wallet_pin()}")
            
            # Test to_dict method
            print(f"\n4. Testing to_dict Method...")
            user_dict = user.to_dict()
            print(f"   PIN locked: {user_dict.get('pin_locked')}")
            print(f"   Lock remaining: {user_dict.get('pin_lock_remaining_minutes')}")
            print(f"   Attempts remaining: {user_dict.get('pin_attempts_remaining')}")
            
            print("\n✅ PIN Status Test Completed Successfully!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_pin_status() 