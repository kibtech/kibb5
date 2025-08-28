#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def test_referral_stats():
    """Test the referral stats functionality"""
    print("🔧 Testing Referral Stats...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Get a user to test with
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return False
            
            print(f"📝 Testing with user: {user.email}")
            print(f"📝 User referral code: {user.referral_code}")
            
            # Check if user has a referral code
            if not user.referral_code:
                print("❌ User has no referral code!")
                return False
            
            # Get referral statistics manually
            total_referrals = len(user.referrals)
            total_commissions = sum(commission.amount for commission in user.commissions_earned)
            
            print(f"📊 Total referrals: {total_referrals}")
            print(f"📊 Total commissions: {total_commissions}")
            print(f"📊 Wallet balance: {user.wallet.balance if user.wallet else 0}")
            
            # Simulate what the API should return
            expected_response = {
                'referral_code': user.referral_code,
                'total_referrals': total_referrals,
                'total_commissions': float(total_commissions),
                'wallet_balance': float(user.wallet.balance) if user.wallet else 0.0
            }
            
            print(f"✅ Expected API response: {expected_response}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing referral stats: {str(e)}")
            return False

if __name__ == "__main__":
    print("🚀 Referral Stats Test Tool")
    print("=" * 50)
    
    success = test_referral_stats()
    
    if success:
        print("\n✅ Referral stats test completed!")
        print("💡 Check the output above to see what the API should return.")
    else:
        print("\n❌ Referral stats test failed. Please check the error above.") 