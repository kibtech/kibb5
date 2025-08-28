#!/usr/bin/env python3
"""
Fix E-commerce Payment Callback Issue
====================================

This script fixes the issue where e-commerce orders don't get updated
and commissions aren't processed in the M-Pesa callback.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Order, Payment, User, Commission, Wallet
from decimal import Decimal
import logging
from datetime import datetime

def fix_ecommerce_callback_issue():
    """Fix e-commerce orders that have completed payments but pending status"""
    print("🔧 Fixing E-commerce Payment Callback Issue")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Step 1: Find all completed payments for e-commerce orders
            print("\n1. 🔍 Finding completed payments for e-commerce orders...")
            
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
                    print(f"      Total Amount: KSh {order.total_amount}")
                    print(f"      User: {order.user.name} (ID: {order.user.id})")
                    print(f"      Referred By: {order.user.referred_by_id}")
                    
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
                        
                        # Process commission if user was referred
                        if order.user.referred_by_id:
                            existing_commission = Commission.query.filter_by(
                                order_id=order.id,
                                commission_type='order'
                            ).first()
                            
                            if not existing_commission:
                                print(f"      💰 Processing commission for referrer...")
                                
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
                                    print(f"      💰 Referrer: {referrer.name} ({referrer.email})")
                                    processed_commissions += 1
                                else:
                                    print(f"      ⚠️ Referrer or wallet not found")
                            else:
                                print(f"      ℹ️ Commission already processed: KSh {existing_commission.amount}")
                        else:
                            print(f"      ℹ️ No referral - no commission to process")
                        
                        fixed_orders += 1
                    else:
                        print(f"      ✅ Order status already correct")
                        
                        # Check if commission was processed
                        if order.user.referred_by_id:
                            existing_commission = Commission.query.filter_by(
                                order_id=order.id,
                                commission_type='order'
                            ).first()
                            
                            if existing_commission:
                                print(f"      💰 Commission already processed: KSh {existing_commission.amount}")
                            else:
                                print(f"      ⚠️ Commission missing for referred user!")
                        else:
                            print(f"      ℹ️ No referral - no commission needed")
                else:
                    print(f"   ⚠️ Payment {payment.id} has no associated order")
            
            # Step 2: Check for orders with pending payment status but completed payments
            print(f"\n2. 🔍 Checking for orders with pending payment status...")
            
            pending_orders = Order.query.filter_by(payment_status='pending').all()
            print(f"   Found {len(pending_orders)} orders with pending payment status")
            
            for order in pending_orders:
                payments = Payment.query.filter_by(order_id=order.id).all()
                print(f"\n   📋 Order: {order.order_number}")
                print(f"      Status: {order.status}")
                print(f"      Payment Status: {order.payment_status}")
                print(f"      Payments: {len(payments)}")
                
                for payment in payments:
                    print(f"         - Payment ID: {payment.id}")
                    print(f"           Status: {payment.status}")
                    print(f"           Amount: KSh {payment.amount}")
                    print(f"           Created: {payment.created_at}")
                    
                    # Check for status mismatch
                    if payment.status == 'completed' and order.payment_status == 'pending':
                        print(f"         ⚠️ STATUS MISMATCH: Payment completed but order still pending!")
                        print(f"         🔧 This order needs fixing!")
            
            # Step 3: Commit all changes
            if fixed_orders > 0:
                db.session.commit()
                print(f"\n✅ Successfully fixed {fixed_orders} orders!")
                print(f"💰 Processed {processed_commissions} new commissions")
            else:
                print(f"\nℹ️ No orders needed fixing")
            
            # Step 4: Verify fixes
            print(f"\n3. 🔍 Verifying fixes...")
            
            # Check payment status distribution
            status_counts = db.session.query(
                Order.payment_status,
                db.func.count(Order.id)
            ).group_by(Order.payment_status).all()
            
            print(f"   Payment Status Distribution:")
            for status, count in status_counts:
                print(f"      {status}: {count}")
            
            # Check commission processing
            commission_counts = db.session.query(
                Commission.commission_type,
                db.func.count(Commission.id)
            ).group_by(Commission.commission_type).all()
            
            print(f"   Commission Distribution:")
            for comm_type, count in commission_counts:
                print(f"      {comm_type}: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing e-commerce callback issue: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_specific_order(order_number):
    """Check a specific order for payment and commission issues"""
    print(f"\n🔍 Checking Specific Order: {order_number}")
    print("=" * 40)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Find the order
            order = Order.query.filter_by(order_number=order_number).first()
            
            if not order:
                print(f"❌ Order {order_number} not found")
                return
            
            print(f"📋 Order Details:")
            print(f"   ID: {order.id}")
            print(f"   Status: {order.status}")
            print(f"   Payment Status: {order.payment_status}")
            print(f"   Total Amount: KSh {order.total_amount}")
            print(f"   Created: {order.created_at}")
            print(f"   User: {order.user.name} ({order.user.email})")
            print(f"   Referred By: {order.user.referred_by_id}")
            
            # Check payments
            payments = Payment.query.filter_by(order_id=order.id).all()
            print(f"\n💳 Payments ({len(payments)}):")
            
            for payment in payments:
                print(f"   - Payment ID: {payment.id}")
                print(f"     Status: {payment.status}")
                print(f"     Amount: KSh {payment.amount}")
                print(f"     Created: {payment.created_at}")
                print(f"     M-Pesa Code: {payment.mpesa_code}")
                
                # Check for status mismatch
                if payment.status == 'completed' and order.payment_status != 'paid':
                    print(f"     ⚠️ STATUS MISMATCH DETECTED!")
            
            # Check commission
            if order.user.referred_by_id:
                commission = Commission.query.filter_by(
                    order_id=order.id,
                    commission_type='order'
                ).first()
                
                print(f"\n💰 Commission:")
                if commission:
                    print(f"   ✅ Commission processed: KSh {commission.amount}")
                    print(f"   Referrer: {commission.referrer.name}")
                else:
                    print(f"   ❌ Commission NOT processed!")
                    print(f"   This is the issue - commission should be processed")
            else:
                print(f"\n💰 Commission: No referral - no commission needed")
                
    except Exception as e:
        print(f"❌ Error checking order: {str(e)}")

if __name__ == "__main__":
    print("🚀 E-commerce Payment Callback Fix Script")
    print("=" * 50)
    
    # Check specific order if provided
    if len(sys.argv) > 1:
        order_number = sys.argv[1]
        check_specific_order(order_number)
    else:
        # Run the full fix
        success = fix_ecommerce_callback_issue()
        if success:
            print("\n🎉 E-commerce callback fix completed successfully!")
            print("\n📋 What was fixed:")
            print("   ✅ Payment status synchronization")
            print("   ✅ Order status updates")
            print("   ✅ Commission processing")
            print("   ✅ Progress tracking updates")
        else:
            print("\n❌ E-commerce callback fix failed!") 