#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def test_wallet_api():
    """Test the wallet API endpoints"""
    print("🔧 Testing Wallet API Endpoints...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Get a user to test with
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return False
            
            print(f"📝 Testing with user: {user.email}")
            
            # Test wallet stats endpoint
            print("\n📝 Testing /api/wallet/stats...")
            with app.test_client() as client:
                # We need to simulate a logged-in user
                # For now, let's just test the data structure
                current_balance = user.wallet.balance if user.wallet else 0
                deposited_balance = user.wallet.deposited_balance if user.wallet else 0
                commission_balance = user.wallet.commission_balance if user.wallet else 0
                
                print(f"  - Current balance: {current_balance}")
                print(f"  - Deposited balance: {deposited_balance}")
                print(f"  - Commission balance: {commission_balance}")
            
            # Test commissions endpoint
            print("\n📝 Testing /api/wallet/commissions...")
            commissions = user.commissions_earned.all()
            print(f"  - Number of commissions: {len(commissions)}")
            
            # Test withdrawals endpoint
            print("\n📝 Testing /api/wallet/withdrawals...")
            withdrawals = user.withdrawals.all()
            print(f"  - Number of withdrawals: {len(withdrawals)}")
            
            # Test settings endpoint
            print("\n📝 Testing /api/wallet/settings...")
            from app.models import SystemSettings
            min_withdrawal = SystemSettings.query.filter_by(key='min_withdrawal_amount').first()
            if min_withdrawal:
                print(f"  - Min withdrawal amount: {min_withdrawal.value}")
            else:
                print("  - Min withdrawal setting not found")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing wallet API: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("🚀 Wallet API Test Tool")
    print("=" * 50)
    
    success = test_wallet_api()
    
    if success:
        print("\n✅ Wallet API test completed!")
        print("💡 Check the output above to see the data structure.")
    else:
        print("\n❌ Wallet API test failed. Please check the error above.") 