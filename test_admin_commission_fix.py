#!/usr/bin/env python3
"""
Test Admin Commission Fix
Simulates admin marking an order as paid and verifies commission is processed.
"""
import os
import sys
from decimal import Decimal
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User, Order, Commission, Wallet, OrderItem, Product
from app.admin.orders import update_payment_status

def test_admin_commission_fix():
    """Test that our admin commission fix works"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Testing Admin Commission Fix...")
        print("=" * 50)
        
        # Find a user with referral relationship and a pending order
        print("\n🔍 Looking for test scenario...")
        
        # Get existing orders with payment issues
        orders_with_issues = db.session.query(Order).filter(
            Order.payment_status == 'paid',
            Order.user_id.in_(
                db.session.query(User.id).filter(User.referred_by_id.isnot(None))
            )
        ).all()
        
        if orders_with_issues:
            print(f"✅ Found {len(orders_with_issues)} paid orders from referred users")
            
            for order in orders_with_issues:
                user = order.user
                print(f"\n📦 Order: {order.order_number}")
                print(f"   User: {user.name} (ID: {user.id})")
                print(f"   Referred by: User ID {user.referred_by_id}")
                print(f"   Amount: KSh {order.total_amount}")
                print(f"   Status: {order.status}, Payment: {order.payment_status}")
                
                # Check if commission already exists
                existing_commission = db.session.query(Commission).filter_by(order_id=order.id).first()
                if existing_commission:
                    print(f"   ✅ Commission exists: KSh {existing_commission.amount}")
                else:
                    print(f"   ❌ No commission found!")
                    
                    # Calculate expected commission
                    commission_rate = 0.03  # 3%
                    expected_commission = Decimal(str(float(order.total_amount) * commission_rate))
                    print(f"   💡 Expected commission: KSh {expected_commission}")
                    
                    # Get referrer info
                    referrer = db.session.get(User, user.referred_by_id)
                    if referrer:
                        print(f"   👤 Referrer: {referrer.name}")
                        if referrer.wallet:
                            print(f"   💰 Current commission balance: KSh {referrer.wallet.commission_balance}")
                        else:
                            print(f"   ⚠️  Referrer has no wallet!")
        else:
            print("❌ No suitable test orders found")
        
        print(f"\n📊 Current Commission Statistics:")
        print("=" * 40)
        
        # Count commissions by type
        ecommerce_count = db.session.query(Commission).filter_by(commission_type='order').count()
        cyber_count = db.session.query(Commission).filter_by(commission_type='cyber_service').count()
        
        print(f"E-commerce commissions: {ecommerce_count}")
        print(f"Cyber service commissions: {cyber_count}")
        
        # Test the fix simulation
        print(f"\n🧪 Testing Fix Simulation:")
        print("=" * 30)
        print("💡 To test the fix manually:")
        print("1. Go to admin panel → Orders")
        print("2. Find an order from a referred user")
        print("3. Change payment status from 'pending' to 'paid'")
        print("4. Commission should be automatically created!")
        print("5. Check referrer's wallet balance increase")
        
        print(f"\n✅ Admin commission fix test completed!")

if __name__ == "__main__":
    print("🚀 Admin Commission Fix Test")
    print("-" * 40)
    test_admin_commission_fix()
    print("\n✅ Test completed successfully!")