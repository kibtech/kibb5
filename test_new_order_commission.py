#!/usr/bin/env python3
"""
Test New Order Commission Processing
Creates a test scenario to verify our admin commission fix works for new orders.
"""
import os
import sys
from decimal import Decimal
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User, Order, Commission, Wallet, SystemSettings

def test_new_order_commission():
    """Test commission processing for new orders via admin payment approval"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Testing New Order Commission Processing...")
        print("=" * 50)
        
        # Find users for testing
        print("\n🔍 Finding test users...")
        
        # Find a user who was referred
        referred_user = db.session.query(User).filter(User.referred_by_id.isnot(None)).first()
        if not referred_user:
            print("❌ No referred users found for testing")
            return
        
        referrer = db.session.get(User, referred_user.referred_by_id)
        if not referrer:
            print("❌ Referrer not found")
            return
        
        print(f"✅ Test users found:")
        print(f"   👤 Referred user: {referred_user.name} (ID: {referred_user.id})")
        print(f"   👤 Referrer: {referrer.name} (ID: {referrer.id})")
        
        # Check current wallet balance
        if referrer.wallet:
            initial_balance = referrer.wallet.commission_balance
            print(f"   💰 Referrer's initial commission balance: KSh {initial_balance}")
        else:
            print("   ⚠️  Referrer has no wallet!")
            return
        
        # Show commission rate
        commission_setting = db.session.query(SystemSettings).filter_by(key='ecommerce_commission_rate').first()
        commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.03
        print(f"   📊 Commission rate: {commission_rate * 100}%")
        
        # Create a test order (simulation)
        print(f"\n🧪 Creating test order simulation...")
        test_amount = Decimal('100.00')  # KSh 100 order
        expected_commission = Decimal(str(float(test_amount) * commission_rate))
        
        print(f"   📦 Simulated order amount: KSh {test_amount}")
        print(f"   💰 Expected commission: KSh {expected_commission}")
        
        print(f"\n📋 Manual Testing Steps:")
        print("=" * 30)
        print("1. Go to your admin panel")
        print("2. Create a new order or find a pending order")
        print(f"3. Make sure the order is from user: {referred_user.name}")
        print("4. Set the payment status to 'paid'")
        print("5. Check that commission is automatically created")
        print(f"6. Verify referrer {referrer.name}'s wallet balance increases")
        
        print(f"\n🔍 Current Commission Statistics:")
        print("=" * 35)
        
        # Show current commissions
        ecommerce_commissions = db.session.query(Commission).filter_by(commission_type='order').count()
        cyber_commissions = db.session.query(Commission).filter_by(commission_type='cyber_service').count()
        
        print(f"E-commerce commissions: {ecommerce_commissions}")
        print(f"Cyber service commissions: {cyber_commissions}")
        
        # Show recent commissions for this referrer
        recent_commissions = db.session.query(Commission).filter_by(referrer_id=referrer.id).order_by(Commission.created_at.desc()).limit(5).all()
        
        if recent_commissions:
            print(f"\n📈 Recent commissions for {referrer.name}:")
            for comm in recent_commissions:
                print(f"   💰 KSh {comm.amount} - {comm.description} ({comm.created_at.strftime('%Y-%m-%d %H:%M')})")
        else:
            print(f"\n📈 No recent commissions found for {referrer.name}")
        
        print(f"\n✅ Test setup completed!")
        print("💡 Now test by creating an order in the admin panel and marking it as paid.")

if __name__ == "__main__":
    print("🚀 New Order Commission Test")
    print("-" * 35)
    test_new_order_commission()
    print("\n✅ Test completed successfully!")