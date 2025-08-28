#!/usr/bin/env python3
"""
Simple test for the referral endpoint
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, db

def test_referral_endpoint():
    """Test the referral endpoint logic"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing Referral Endpoint Logic...")
        print("=" * 50)
        
        # Find user JOY
        user = db.session.query(User).filter_by(name='JOY').first()
        if not user:
            print("❌ User 'JOY' not found!")
            return False
        
        print(f"✅ Found user: {user.name}")
        print(f"   User ID: {user.id}")
        print(f"   Referral Code: {user.referral_code}")
        
        # Test the logic that the endpoint uses
        from app.auth.routes import referral_stats
        
        # Mock the JWT context
        from flask import g
        g.user_id = user.id
        
        try:
            # This would normally require proper JWT setup
            print(f"\n🔍 Testing endpoint logic...")
            
            # Manually test the database queries
            total_referrals = db.session.query(User).filter_by(referred_by_id=user.id).count()
            print(f"   Total Referrals: {total_referrals}")
            
            from app.models import Commission
            total_commissions = db.session.query(db.func.sum(Commission.amount))\
                .filter_by(referrer_id=user.id).scalar() or 0
            print(f"   Total Commissions: {total_commissions}")
            
            # Simulate the response
            response_data = {
                'referral_code': user.referral_code,
                'total_referrals': total_referrals,
                'total_earned': float(total_commissions),
                'total_commissions': float(total_commissions),
                'wallet_balance': float(user.wallet.balance) if user.wallet else 0.0
            }
            
            print(f"\n📊 Simulated API Response:")
            print(f"   {response_data}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing endpoint: {str(e)}")
            return False

if __name__ == "__main__":
    print("🚀 Referral Endpoint Tester")
    print("=" * 50)
    
    try:
        success = test_referral_endpoint()
        if success:
            print("\n✅ Test completed successfully!")
        else:
            print("\n❌ Test failed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 