#!/usr/bin/env python3
"""
Fix Stuck Payment
This script manually completes a stuck payment for testing purposes.
Use this only for testing - in production, the MPesa callback should handle this.
"""

import os
import sys
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import CyberServiceOrder, User, Commission, SystemSettings
from decimal import Decimal
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_stuck_payment():
    """Fix the stuck payment manually for testing"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 FIXING STUCK PAYMENT MANUALLY")
        print("=" * 50)
        
        # Find the stuck order
        order_number = "CS2025081320430924"
        order = CyberServiceOrder.query.filter_by(order_number=order_number).first()
        
        if not order:
            print(f"❌ Order {order_number} not found")
            return
        
        print(f"📦 Order Details:")
        print(f"   Order Number: {order.order_number}")
        print(f"   Current Status: {order.status}")
        print(f"   Current Payment Status: {order.payment_status}")
        print(f"   Amount: KSh {order.amount}")
        print(f"   User: {order.user.email if order.user else 'Unknown'}")
        
        # Check if user was referred
        if order.user and order.user.referred_by_id:
            referrer = User.query.get(order.user.referred_by_id)
            print(f"   Referred by: {referrer.email if referrer else 'Unknown'}")
            print(f"   Referral Code: {order.user.referral_code}")
        else:
            print(f"   Referred by: No referral relationship")
        
        # Check if payment is already completed
        if order.payment_status == 'paid':
            print(f"\n✅ Payment is already completed!")
            return
        
        print(f"\n🔧 MANUALLY COMPLETING PAYMENT...")
        
        # Update payment status
        order.payment_status = 'paid'
        order.status = 'paid'
        order.paid_at = datetime.utcnow()
        order.updated_at = datetime.utcnow()
        
        # Add a dummy MPesa code for testing
        order.mpesa_code = f"TEST{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        print(f"   ✅ Payment status updated to 'paid'")
        print(f"   ✅ Order status updated to 'paid'")
        print(f"   ✅ Payment timestamp added")
        print(f"   ✅ Test MPesa code added: {order.mpesa_code}")
        
        # Process commission if user was referred
        if order.user and order.user.referred_by_id:
            print(f"\n💰 PROCESSING COMMISSION...")
            
            # Get commission rate
            commission_setting = SystemSettings.query.filter_by(
                key='cyber_services_commission_rate'
            ).first()
            commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.20
            
            commission_amount = Decimal(str(float(order.amount) * commission_rate))
            
            # Check if commission already exists
            existing_commission = Commission.query.filter_by(order_id=order.id).first()
            
            if existing_commission:
                print(f"   ⚠️  Commission already exists: KSh {existing_commission.amount}")
            else:
                # Create commission record
                commission = Commission(
                    referrer_id=order.user.referred_by_id,
                    order_id=order.id,
                    amount=commission_amount,
                    commission_type='order',
                    description=f'Commission from cyber service order {order.order_number} (manual fix)'
                )
                db.session.add(commission)
                
                # Update referrer's wallet
                referrer = User.query.get(order.user.referred_by_id)
                if referrer and referrer.wallet:
                    referrer.wallet.add_commission(commission_amount)
                    print(f"   ✅ Commission processed: KSh {commission_amount}")
                    print(f"   ✅ Added to referrer wallet: {referrer.email}")
                else:
                    print(f"   ❌ Could not add commission to wallet")
        else:
            print(f"\n💰 NO COMMISSION: User was not referred")
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n🎉 PAYMENT MANUALLY COMPLETED!")
        print(f"   Order {order.order_number} is now marked as paid")
        print(f"   Commission has been processed (if applicable)")
        print(f"   Referral system should now work for this order")
        
        # Verify the fix
        print(f"\n🔍 VERIFICATION:")
        updated_order = CyberServiceOrder.query.filter_by(order_number=order_number).first()
        print(f"   Payment Status: {updated_order.payment_status}")
        print(f"   Order Status: {updated_order.status}")
        print(f"   MPesa Code: {updated_order.mpesa_code}")
        
        if updated_order.user and updated_order.user.referred_by_id:
            commission = Commission.query.filter_by(order_id=updated_order.id).first()
            if commission:
                print(f"   Commission: KSh {commission.amount} processed")
            else:
                print(f"   Commission: Not processed")

if __name__ == "__main__":
    try:
        fix_stuck_payment()
        
    except Exception as e:
        logger.error(f"Failed to fix stuck payment: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 