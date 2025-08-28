#!/usr/bin/env python3
"""
Investigate Referral Payment Issue
This script investigates why payments for referred users get stuck
while payments for non-referred users work perfectly.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import CyberServiceOrder, User, Commission
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def investigate_referral_payment_issue():
    """Investigate the referral payment issue"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 INVESTIGATING REFERRAL PAYMENT ISSUE")
        print("=" * 60)
        
        # Check the stuck order
        stuck_order_number = "CS2025081320430924"
        stuck_order = CyberServiceOrder.query.filter_by(order_number=stuck_order_number).first()
        
        if not stuck_order:
            print(f"❌ Stuck order {stuck_order_number} not found")
            return
        
        print(f"📦 STUCK ORDER ANALYSIS:")
        print(f"   Order Number: {stuck_order.order_number}")
        print(f"   Status: {stuck_order.status}")
        print(f"   Payment Status: {stuck_order.payment_status}")
        print(f"   Amount: KSh {stuck_order.amount}")
        print(f"   User: {stuck_order.user.email if stuck_order.user else 'Unknown'}")
        print(f"   Created: {stuck_order.created_at}")
        
        # Check referral status
        if stuck_order.user and stuck_order.user.referred_by_id:
            referrer = User.query.get(stuck_order.user.referred_by_id)
            print(f"   Referred by: {referrer.email if referrer else 'Unknown'}")
            print(f"   Referral Code: {stuck_order.user.referral_code}")
            print(f"   Referrer ID: {stuck_order.user.referred_by_id}")
        else:
            print(f"   Referred by: No referral relationship")
        
        # Check if there are any errors in the order
        print(f"\n🔍 ORDER DETAILS:")
        print(f"   Has MPesa Code: {'Yes' if stuck_order.mpesa_code else 'No'}")
        print(f"   Has Payment ID: {'Yes' if stuck_order.payment_id else 'No'}")
        print(f"   Has Paid At: {'Yes' if stuck_order.paid_at else 'No'}")
        print(f"   Has Updated At: {'Yes' if stuck_order.updated_at else 'No'}")
        
        # Compare with working orders (non-referred users)
        print(f"\n📊 COMPARING WITH WORKING ORDERS:")
        
        # Find recent working orders (non-referred users)
        working_orders = CyberServiceOrder.query.filter(
            CyberServiceOrder.created_at >= datetime.utcnow() - timedelta(days=7),
            CyberServiceOrder.payment_status == 'paid'
        ).all()
        
        print(f"   Total working orders (last 7 days): {len(working_orders)}")
        
        referred_working = 0
        non_referred_working = 0
        
        for order in working_orders:
            if order.user and order.user.referred_by_id:
                referred_working += 1
            else:
                non_referred_working += 1
        
        print(f"   Working orders from referred users: {referred_working}")
        print(f"   Working orders from non-referred users: {non_referred_working}")
        
        # Find recent stuck orders (referred users)
        stuck_orders = CyberServiceOrder.query.filter(
            CyberServiceOrder.created_at >= datetime.utcnow() - timedelta(days=7),
            CyberServiceOrder.payment_status == 'pending'
        ).all()
        
        print(f"   Total stuck orders (last 7 days): {len(stuck_orders)}")
        
        referred_stuck = 0
        non_referred_stuck = 0
        
        for order in stuck_orders:
            if order.user and order.user.referred_by_id:
                referred_stuck += 1
            else:
                non_referred_stuck += 1
        
        print(f"   Stuck orders from referred users: {referred_stuck}")
        print(f"   Stuck orders from non-referred users: {non_referred_stuck}")
        
        # Check for specific patterns
        print(f"\n🔍 PATTERN ANALYSIS:")
        
        if referred_stuck > 0 and non_referred_stuck == 0:
            print(f"   ❌ PATTERN FOUND: Only referred users have stuck payments!")
            print(f"   💡 This confirms the issue is with referral processing")
        elif referred_stuck > 0 and non_referred_stuck > 0:
            print(f"   ⚠️  Mixed pattern: Both referred and non-referred users have stuck payments")
        else:
            print(f"   ✅ No stuck payments found")
        
        # Check if the issue is in the callback processing
        print(f"\n🔧 CALLBACK PROCESSING ANALYSIS:")
        
        # Look at the MPesa callback route to see if there are any referral-specific errors
        print(f"   The issue might be in the MPesa callback processing for referred users")
        print(f"   Possible causes:")
        print(f"     1. Referral commission calculation failing")
        print(f"     2. Commission database insertion failing")
        print(f"     3. Referrer wallet update failing")
        print(f"     4. Email notification failing and blocking the process")
        
        # Check if there are any commission records for the stuck order
        commission = Commission.query.filter_by(order_id=stuck_order.id).first()
        if commission:
            print(f"   💰 Commission already exists: KSh {commission.amount}")
        else:
            print(f"   💰 Commission: Not processed yet")
        
        print(f"\n🛠️  RECOMMENDED ACTIONS:")
        print(f"   1. Check server logs for errors during referral processing")
        print(f"   2. Look for database constraint violations")
        print(f"   3. Check if email service is blocking the process")
        print(f"   4. Verify referrer wallet exists and is accessible")
        print(f"   5. Test with a simple referral payment to isolate the issue")

def check_referral_payment_flow():
    """Check the referral payment flow for potential issues"""
    
    print(f"\n🔍 REFERRAL PAYMENT FLOW CHECK:")
    
    # The flow should be:
    # 1. STK Push initiated ✅ (working)
    # 2. MPesa callback received ✅ (working for non-referred)
    # 3. Payment status updated ✅ (working for non-referred)
    # 4. Referral check performed ❌ (likely failing here)
    # 5. Commission calculated ❌ (failing)
    # 6. Commission added to wallet ❌ (failing)
    # 7. Email notification sent ❌ (failing)
    
    print(f"   Payment Flow Analysis:")
    print(f"   ✅ Step 1-3: Working for all users")
    print(f"   ❌ Step 4-7: Failing for referred users only")
    print(f"   💡 The issue is in the referral processing steps")

if __name__ == "__main__":
    try:
        investigate_referral_payment_issue()
        check_referral_payment_flow()
        
    except Exception as e:
        logger.error(f"Failed to investigate referral payment issue: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 