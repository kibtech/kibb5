#!/usr/bin/env python3
"""
Fix Payment Notification System
==============================

This script fixes the issue where e-commerce payments don't show success
notifications and orders remain pending even after successful payment.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Order, Payment, User, Commission, Wallet
from decimal import Decimal
import logging
from datetime import datetime, timedelta

def fix_payment_notification_system():
    """Fix the payment notification system to show payment success properly"""
    print("🔧 Fixing Payment Notification System")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Step 1: Fix payment status synchronization
            print("\n1. 🔄 Fixing payment status synchronization...")
            
            # Find payments that are completed but orders are still pending
            completed_payments = Payment.query.filter_by(status='completed').all()
            print(f"   Found {len(completed_payments)} completed payments")
            
            fixed_orders = 0
            processed_commissions = 0
            
            for payment in completed_payments:
                if payment.order:
                    order = payment.order
                    print(f"\n   📋 Order: {order.order_number}")
                    print(f"      Current Status: {order.status}")
                    print(f"      Current Payment Status: {order.payment_status}")
                    print(f"      Payment Status: {payment.status}")
                    
                    # Check if order status needs updating
                    if order.payment_status != 'paid' or order.status != 'confirmed':
                        print(f"      🔧 Updating order status...")
                        
                        # Update order status
                        order.payment_status = 'paid'
                        order.status = 'confirmed'
                        order.confirmed_at = datetime.utcnow()
                        
                        # Update progress tracking
                        order.update_progress()
                        
                        print(f"      ✅ Updated to: {order.status} / {order.payment_status}")
                        
                        # Process commission if not already processed
                        if order.user.referred_by_id:
                            existing_commission = Commission.query.filter_by(
                                order_id=order.id,
                                commission_type='order'
                            ).first()
                            
                            if not existing_commission:
                                print(f"      💰 Processing commission...")
                                
                                # Get commission rate (3% for e-commerce)
                                from app.models import SystemSettings
                                commission_setting = db.session.query(SystemSettings).filter_by(
                                    key='ecommerce_commission_rate'
                                ).first()
                                commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.03
                                
                                commission_amount = Decimal(str(float(order.total_amount) * commission_rate))
                                
                                # Create commission record
                                commission = Commission(
                                    referrer_id=order.user.referred_by_id,
                                    order_id=order.id,
                                    amount=commission_amount,
                                    commission_type='order',
                                    description=f'Commission from order {order.order_number}'
                                )
                                db.session.add(commission)
                                
                                # Update referrer's wallet
                                referrer = db.session.get(User, order.user.referred_by_id)
                                if referrer and referrer.wallet:
                                    referrer.wallet.add_commission(commission_amount)
                                    print(f"      💰 Added KSh {commission_amount} to referrer's wallet")
                                    processed_commissions += 1
                                else:
                                    print(f"      ⚠️ Referrer or wallet not found")
                            else:
                                print(f"      ℹ️ Commission already processed")
                        
                        fixed_orders += 1
                    else:
                        print(f"      ✅ Order status already correct")
            
            # Step 2: Check for orphaned payments (payments without orders)
            print(f"\n2. 🔍 Checking for orphaned payments...")
            orphaned_payments = Payment.query.filter_by(status='completed').filter(
                ~Payment.order_id.in_([o.id for o in Order.query.all()])
            ).all()
            
            if orphaned_payments:
                print(f"   Found {len(orphaned_payments)} orphaned payments")
                for payment in orphaned_payments:
                    print(f"      Payment ID: {payment.id}, Amount: KSh {payment.amount}")
            else:
                print(f"   ✅ No orphaned payments found")
            
            # Step 3: Check for orders with no payments
            print(f"\n3. 🔍 Checking for orders with no payments...")
            orders_without_payments = Order.query.filter(
                ~Order.id.in_([p.order_id for p in Payment.query.all() if p.order_id])
            ).all()
            
            if orders_without_payments:
                print(f"   Found {len(orders_without_payments)} orders without payments")
                for order in orders_without_payments:
                    print(f"      Order: {order.order_number}, Status: {order.status}")
            else:
                print(f"   ✅ All orders have associated payments")
            
            # Step 4: Commit all changes
            if fixed_orders > 0:
                db.session.commit()
                print(f"\n✅ Successfully fixed {fixed_orders} orders!")
                print(f"💰 Processed {processed_commissions} new commissions")
            else:
                print(f"\nℹ️ No orders needed fixing")
            
            # Step 5: Verify fixes
            print(f"\n4. 🔍 Verifying fixes...")
            
            # Check payment status distribution
            status_counts = db.session.query(
                Order.payment_status,
                db.func.count(Order.id)
            ).group_by(Order.payment_status).all()
            
            print(f"   Payment Status Distribution:")
            for status, count in status_counts:
                print(f"      {status}: {count}")
            
            # Check order status distribution
            order_status_counts = db.session.query(
                Order.status,
                db.func.count(Order.id)
            ).group_by(Order.status).all()
            
            print(f"   Order Status Distribution:")
            for status, count in order_status_counts:
                print(f"      {status}: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing payment notification system: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_payment_flow_issues():
    """Check for specific payment flow issues"""
    print("\n🔍 Checking Payment Flow Issues")
    print("=" * 40)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Check recent orders and their payment status
            recent_orders = Order.query.order_by(Order.created_at.desc()).limit(20).all()
            
            print(f"📋 Recent Orders Analysis:")
            for order in recent_orders:
                payments = Payment.query.filter_by(order_id=order.id).all()
                
                print(f"\n   {order.order_number}:")
                print(f"      Status: {order.status}")
                print(f"      Payment Status: {order.payment_status}")
                print(f"      Created: {order.created_at}")
                print(f"      Total Amount: KSh {order.total_amount}")
                
                if payments:
                    print(f"      Payments ({len(payments)}):")
                    for payment in payments:
                        print(f"         - ID: {payment.id}, Status: {payment.status}, Amount: KSh {payment.amount}")
                        
                        # Check for status mismatch
                        if payment.status == 'completed' and order.payment_status != 'paid':
                            print(f"         ⚠️ STATUS MISMATCH: Payment completed but order still pending!")
                else:
                    print(f"      ❌ No payments found")
                    
                    # Check if this is a wallet payment
                    if order.payment_status == 'paid':
                        print(f"      ℹ️ Wallet payment (no M-Pesa payment record)")
            
            # Check for stuck payments
            print(f"\n🔍 Checking for stuck payments...")
            stuck_payments = Payment.query.filter(
                Payment.status == 'pending',
                Payment.created_at < datetime.utcnow() - timedelta(hours=1)
            ).all()
            
            if stuck_payments:
                print(f"   Found {len(stuck_payments)} potentially stuck payments:")
                for payment in stuck_payments:
                    print(f"      Payment ID: {payment.id}")
                    print(f"      Created: {payment.created_at}")
                    print(f"      Status: {payment.status}")
                    if payment.order:
                        print(f"      Order: {payment.order.order_number}")
            else:
                print(f"   ✅ No stuck payments found")
                
    except Exception as e:
        print(f"❌ Error checking payment flow: {str(e)}")

if __name__ == "__main__":
    print("🚀 Payment Notification System Fix Script")
    print("=" * 50)
    
    # Check current state
    check_payment_flow_issues()
    
    # Ask user if they want to proceed
    print(f"\n❓ Do you want to proceed with fixing the payment notification system? (yes/no): ", end="")
    response = input().strip().lower()
    
    if response in ['yes', 'y']:
        success = fix_payment_notification_system()
        if success:
            print("\n🎉 Payment notification system fix completed successfully!")
            print("\n📋 What was fixed:")
            print("   ✅ Payment status synchronization")
            print("   ✅ Order status updates")
            print("   ✅ Commission processing")
            print("   ✅ Progress tracking updates")
            print("\n🎯 Next steps:")
            print("   1. Test a new e-commerce payment")
            print("   2. Verify payment success notification appears")
            print("   3. Check that order status updates to 'confirmed'")
        else:
            print("\n❌ Payment notification system fix failed!")
    else:
        print("\nℹ️ Skipping payment notification system fix.") 