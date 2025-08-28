#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, SystemSettings

def test_wallet_endpoints():
    """Test if wallet endpoints are accessible"""
    print("🔧 Testing Wallet Endpoints...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test if we can access the wallet blueprint
            print("📝 Testing wallet blueprint registration...")
            
            # Check if the blueprint is registered
            wallet_bp = None
            for blueprint_name, blueprint in app.blueprints.items():
                if blueprint_name == 'wallet':
                    wallet_bp = blueprint
                    break
            
            if wallet_bp:
                print("✅ Wallet blueprint is registered")
                print(f"📝 Blueprint URL prefix: {wallet_bp.url_prefix}")
                print(f"📝 Blueprint routes: {list(wallet_bp.deferred_functions)}")
            else:
                print("❌ Wallet blueprint is not registered!")
                return False
            
            # Test if we can access wallet-related models
            print("\n📝 Testing wallet models...")
            user = User.query.first()
            if user:
                print(f"✅ User found: {user.email}")
                print(f"📝 User wallet: {user.wallet}")
                if user.wallet:
                    print(f"📝 Wallet balance: {user.wallet.balance}")
                else:
                    print("📝 User has no wallet")
            else:
                print("❌ No users found")
            
            # Test system settings
            print("\n📝 Testing system settings...")
            min_withdrawal = SystemSettings.query.filter_by(key='min_withdrawal_amount').first()
            if min_withdrawal:
                print(f"✅ Min withdrawal setting found: {min_withdrawal.value}")
            else:
                print("❌ Min withdrawal setting not found")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing wallet endpoints: {str(e)}")
            return False

if __name__ == "__main__":
    print("🚀 Wallet Endpoints Test Tool")
    print("=" * 50)
    
    success = test_wallet_endpoints()
    
    if success:
        print("\n✅ Wallet endpoints test completed!")
        print("💡 Check the output above to see if wallet routes are properly set up.")
    else:
        print("\n❌ Wallet endpoints test failed. Please check the error above.") 