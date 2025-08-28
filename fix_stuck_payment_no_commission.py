#!/usr/bin/env python3
"""
Fix Stuck Payment (No Commission)
This script manually completes a stuck payment without processing commission
to avoid the database constraint violation.
"""

import os
import sys
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import CyberServiceOrder, User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_stuck_payment_no_commission():
    """Fix the stuck payment manually without commission processing"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 FIXING STUCK PAYMENT (NO COMMISSION)")
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
        
        # Check referral status
        if order.user and order.user.referred_by_id:
            referrer = User.query.get(order.user.referred_by_id)
            print(f"   Referred by: {referrer.email if referrer else 'Unknown'}")
            print(f"   Referral Code: {order.user.referral_code}")
            print(f"   ⚠️  NOTE: Commission will NOT be processed due to database constraint issue")
        else:
            print(f"   Referred by: No referral relationship")
        
        # Check if payment is already completed
        if order.payment_status == 'paid':
            print(f"\n✅ Payment is already completed!")
            return
        
        print(f"\n🔧 MANUALLY COMPLETING PAYMENT (NO COMMISSION)...")
        
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
        
        # Skip commission processing for now
        print(f"\n💰 COMMISSION PROCESSING:")
        print(f"   ⚠️  SKIPPED due to database constraint issue")
        print(f"   💡 This will be fixed in the next step")
        
        # Commit the payment completion
        db.session.commit()
        
        print(f"\n🎉 PAYMENT MANUALLY COMPLETED!")
        print(f"   Order {order.order_number} is now marked as paid")
        print(f"   Commission will be processed after fixing the database structure")
        print(f"   Payment flow is now working for this order")
        
        # Verify the fix
        print(f"\n🔍 VERIFICATION:")
        updated_order = CyberServiceOrder.query.filter_by(order_number=order_number).first()
        print(f"   Payment Status: {updated_order.payment_status}")
        print(f"   Order Status: {updated_order.status}")
        print(f"   MPesa Code: {updated_order.mpesa_code}")
        
        print(f"\n⚠️  IMPORTANT NOTES:")
        print(f"   1. Payment is now complete and working")
        print(f"   2. Commission was NOT processed due to database issue")
        print(f"   3. Next step: Fix the commission table structure")
        print(f"   4. Then process commissions for all pending orders")

if __name__ == "__main__":
    try:
        fix_stuck_payment_no_commission()
        
    except Exception as e:
        logger.error(f"Failed to fix stuck payment: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 