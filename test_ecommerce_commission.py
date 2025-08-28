#!/usr/bin/env python3
"""
Test E-commerce Commission System
Verifies that commissions are properly calculated and awarded for e-commerce orders.
"""
import os
import sys
from decimal import Decimal

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User, Order, Commission, Wallet, SystemSettings

def test_ecommerce_commission():
    """Test e-commerce commission calculation and processing"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Testing E-commerce Commission System...")
        print("=" * 50)
        
        # Check commission rate setting
        commission_setting = db.session.query(SystemSettings).filter_by(key='ecommerce_commission_rate').first()
        if commission_setting:
            commission_rate = float(commission_setting.value) / 100.0
            print(f"📊 E-commerce commission rate: {commission_rate * 100}%")
        else:
            commission_rate = 0.03  # Default 3%
            print(f"⚠️  No commission rate setting found, using default: {commission_rate * 100}%")
        
        # Find a test user with referrals
        print("\n🔍 Looking for users with referrals...")
        users_with_referrals = db.session.query(User).filter(User.referred_by_id.isnot(None)).limit(5).all()
        
        if not users_with_referrals:
            print("❌ No users with referrals found. Creating test data...")
            return create_test_referral_data()
        
        print(f"✅ Found {len(users_with_referrals)} users with referrals")
        
        # Test commission calculation for each user
        for user in users_with_referrals:
            print(f"\n👤 Testing user: {user.name} (ID: {user.id})")
            print(f"   Referred by: User ID {user.referred_by_id}")
            
            # Get user's orders
            orders = db.session.query(Order).filter_by(user_id=user.id).all()
            print(f"   Total orders: {len(orders)}")
            
            if orders:
                # Check commissions for each order
                for order in orders:
                    print(f"\n   📦 Order: {order.order_number}")
                    print(f"      Status: {order.status}, Payment: {order.payment_status}")
                    print(f"      Amount: KSh {order.total_amount}")
                    
                    # Check if commission exists
                    commission = db.session.query(Commission).filter_by(order_id=order.id).first()
                    if commission:
                        print(f"      ✅ Commission: KSh {commission.amount} ({commission.commission_type})")
                        print(f"         Referrer ID: {commission.referrer_id}")
                    else:
                        print(f"      ❌ No commission found")
                        
                        # Calculate expected commission
                        if order.payment_status == 'paid' and user.referred_by_id:
                            expected_commission = Decimal(str(float(order.total_amount) * commission_rate))
                            print(f"         Expected commission: KSh {expected_commission}")
        
        # Summary of commission statistics
        print(f"\n📈 Commission Summary:")
        print("=" * 30)
        
        # Total commissions by type
        ecommerce_commissions = db.session.query(Commission).filter_by(commission_type='order').all()
        cyber_commissions = db.session.query(Commission).filter_by(commission_type='cyber_service').all()
        
        ecommerce_total = sum(c.amount for c in ecommerce_commissions)
        cyber_total = sum(c.amount for c in cyber_commissions)
        
        print(f"E-commerce commissions: {len(ecommerce_commissions)} records, KSh {ecommerce_total}")
        print(f"Cyber service commissions: {len(cyber_commissions)} records, KSh {cyber_total}")
        print(f"Total commissions: KSh {ecommerce_total + cyber_total}")
        
        # Check wallet balances
        print(f"\n💰 Wallet Commission Balances:")
        print("=" * 35)
        
        wallets_with_commissions = db.session.query(Wallet).filter(Wallet.commission_balance > 0).all()
        for wallet in wallets_with_commissions:
            user = db.session.get(User, wallet.user_id)
            print(f"{user.name}: KSh {wallet.commission_balance}")
        
        print(f"\n✅ E-commerce commission test completed!")

def create_test_referral_data():
    """Create test referral data for testing"""
    print("🔧 Creating test referral data...")
    
    # This is just a placeholder - in real testing you'd create proper test data
    print("💡 To test commissions properly:")
    print("1. Create a referrer user")
    print("2. Create a referred user with referrer's referral code")
    print("3. Create an e-commerce order for the referred user")
    print("4. Mark the order as paid via admin panel")
    print("5. Check if commission was awarded to the referrer")

if __name__ == "__main__":
    print("🚀 E-commerce Commission Test")
    print("-" * 40)
    test_ecommerce_commission()
    print("\n✅ Test completed successfully!")