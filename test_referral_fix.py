#!/usr/bin/env python3
"""
Test script to verify the referral endpoint fix
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, Commission, Wallet, db

def test_referral_fix():
    """Test the referral endpoint fix"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing Referral Endpoint Fix...")
        print("=" * 50)
        
        # Find user JOY
        user = db.session.query(User).filter_by(name='JOY').first()
        if not user:
            print("❌ User 'JOY' not found!")
            return False
        
        print(f"✅ Found user: {user.name}")
        print(f"   User ID: {user.id}")
        print(f"   Referral Code: {user.referral_code}")
        print(f"   Has Wallet: {user.wallet is not None}")
        
        if user.wallet:
            print(f"   Wallet Balance: {user.wallet.balance}")
        else:
            print("   Creating wallet for user...")
            wallet = Wallet(user_id=user.id)
            db.session.add(wallet)
            db.session.commit()
            print("   ✅ Wallet created")
        
        # Test the database queries that the endpoint uses
        print(f"\n🔍 Testing database queries...")
        
        try:
            # Test referral count
            total_referrals = db.session.query(User).filter_by(referred_by_id=user.id).count()
            print(f"   Total Referrals: {total_referrals}")
            
            # Test commission sum
            total_commissions = db.session.query(db.func.sum(Commission.amount))\
                .filter_by(referrer_id=user.id).scalar() or 0
            print(f"   Total Commissions: {total_commissions}")
            
            # Test wallet access
            wallet_balance = float(user.wallet.balance) if user.wallet else 0.0
            print(f"   Wallet Balance: {wallet_balance}")
            
            print(f"\n✅ All database queries working!")
            
            # Simulate the response
            response_data = {
                'referral_code': user.referral_code,
                'total_referrals': total_referrals,
                'total_earned': float(total_commissions),
                'total_commissions': float(total_commissions),
                'wallet_balance': wallet_balance
            }
            
            print(f"\n📊 Simulated API Response:")
            for key, value in response_data.items():
                print(f"   {key}: {value}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in database queries: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("🚀 Referral Fix Tester")
    print("=" * 50)
    
    try:
        success = test_referral_fix()
        if success:
            print("\n✅ Test completed successfully!")
            print("\n🔥 Now restart your Flask server and test the dashboard!")
        else:
            print("\n❌ Test failed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 