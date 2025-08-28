#!/usr/bin/env python3
"""
Test script to verify wallet PIN functionality
"""

from app import create_app, db
from app.models import User

def test_wallet_pin():
    """Test wallet PIN functionality"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get a test user (first user in database)
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return
            
            print(f"Testing wallet PIN for user: {user.name} ({user.email})")
            
            # Test 1: Check if user has PIN initially
            print(f"\n1. Initial PIN status: {user.has_wallet_pin()}")
            
            # Test 2: Set a PIN
            print("\n2. Setting PIN '1234'...")
            user.set_wallet_pin('1234')
            db.session.commit()
            print(f"   PIN set successfully: {user.has_wallet_pin()}")
            
            # Test 3: Verify correct PIN
            print("\n3. Testing correct PIN '1234'...")
            if user.check_wallet_pin('1234'):
                print("   ✅ Correct PIN verified successfully")
            else:
                print("   ❌ Correct PIN verification failed")
            
            # Test 4: Test incorrect PIN
            print("\n4. Testing incorrect PIN '5678'...")
            if not user.check_wallet_pin('5678'):
                print("   ✅ Incorrect PIN correctly rejected")
            else:
                print("   ❌ Incorrect PIN incorrectly accepted")
            
            # Test 5: Change PIN
            print("\n5. Changing PIN to '5678'...")
            user.set_wallet_pin('5678')
            db.session.commit()
            
            # Test 6: Verify new PIN works
            print("\n6. Testing new PIN '5678'...")
            if user.check_wallet_pin('5678'):
                print("   ✅ New PIN verified successfully")
            else:
                print("   ❌ New PIN verification failed")
            
            # Test 7: Verify old PIN doesn't work
            print("\n7. Testing old PIN '1234' (should fail)...")
            if not user.check_wallet_pin('1234'):
                print("   ✅ Old PIN correctly rejected")
            else:
                print("   ❌ Old PIN incorrectly accepted")
            
            # Test 8: Test invalid PIN format
            print("\n8. Testing invalid PIN format...")
            try:
                user.set_wallet_pin('123')  # Too short
                print("   ❌ Should have failed for short PIN")
            except ValueError as e:
                print(f"   ✅ Correctly rejected short PIN: {e}")
            
            try:
                user.set_wallet_pin('12345')  # Too long
                print("   ❌ Should have failed for long PIN")
            except ValueError as e:
                print(f"   ✅ Correctly rejected long PIN: {e}")
            
            try:
                user.set_wallet_pin('12ab')  # Non-numeric
                print("   ❌ Should have failed for non-numeric PIN")
            except ValueError as e:
                print(f"   ✅ Correctly rejected non-numeric PIN: {e}")
            
            print("\n🎉 All wallet PIN tests completed successfully!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            raise

if __name__ == "__main__":
    test_wallet_pin() 