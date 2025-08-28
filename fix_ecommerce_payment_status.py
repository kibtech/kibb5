#!/usr/bin/env python3
"""
Fix E-commerce Payment Status Issue
===================================

This script fixes the issue where e-commerce orders remain in 'pending' 
payment status even after successful M-Pesa payment.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Order, Payment, User, Commission, Wallet
from decimal import Decimal
import logging

def fix_ecommerce_payment_status():
    """Fix e-commerce orders that have completed payments but pending status"""
    print("🔧 Fixing E-commerce Payment Status Issues")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Find orders with pending payment status but completed payments
            print("\n1. 🔍 Finding orders with payment status issues...")
            
            # Get all pending orders
            pending_orders = Order.query.filter_by(payment_status='pending').all()
            print(f"   Found {len(pending_orders)} orders with pending payment status")
            
            fixed_count = 0
            commission_processed = 0
            
            for order in pending_orders:
                print(f"\n   📋 Order: {order.order_number}")
                print(f"      Status: {order.status}")
                print(f"      Payment Status: {order.payment_status}")
                print(f"      Total Amount: KSh {order.total_amount}")
                
                # Check if there are completed payments for this order
                completed_payments = Payment.query.filter_by(
                    order_id=order.id,
                    status='completed'
                ).all()
                
                if completed_payments:
                    print(f"      ✅ Found {len(completed_payments)} completed payments")
                    
                    # Update order status
                    order.payment_status = 'paid'
                    order.status = 'confirmed'
                    
                    # Update progress tracking
                    order.update_progress()
                    
                    print(f"      🔧 Updated order status to: {order.status}")
                    print(f"      🔧 Updated payment status to: {order.payment_status}")
                    
                    # Process commission if not already processed
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
                                commission_processed += 1
                            else:
                                print(f"      ⚠️ Referrer or wallet not found")
                        else:
                            print(f"      ℹ️ Commission already processed")
                    
                    fixed_count += 1
                else:
                    print(f"      ⚠️ No completed payments found")
                    
                    # Check if there are any payments at all
                    all_payments = Payment.query.filter_by(order_id=order.id).all()
                    if all_payments:
                        print(f"      📊 Payment details:")
                        for payment in all_payments:
                            print(f"         Payment ID: {payment.id}")
                            print(f"         Status: {payment.status}")
                            print(f"         Amount: KSh {payment.amount}")
                            print(f"         Created: {payment.created_at}")
                    else:
                        print(f"      ❌ No payments found for this order")
            
            # Commit all changes
            if fixed_count > 0:
                db.session.commit()
                print(f"\n✅ Successfully fixed {fixed_count} orders!")
                print(f"💰 Processed {commission_processed} new commissions")
            else:
                print(f"\nℹ️ No orders needed fixing")
            
            # Show summary
            print(f"\n📊 Summary:")
            print(f"   Total pending orders checked: {len(pending_orders)}")
            print(f"   Orders fixed: {fixed_count}")
            print(f"   Commissions processed: {commission_processed}")
            
            # Verify fixes
            print(f"\n🔍 Verifying fixes...")
            remaining_pending = Order.query.filter_by(payment_status='pending').count()
            print(f"   Remaining pending orders: {remaining_pending}")
            
            if remaining_pending == 0:
                print("   🎉 All payment status issues resolved!")
            else:
                print(f"   ⚠️ {remaining_pending} orders still pending - may need manual review")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing payment status: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_payment_flow():
    """Check the current payment flow to identify issues"""
    print("\n🔍 Checking Payment Flow")
    print("=" * 30)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Check recent orders
            recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
            
            print(f"📋 Recent orders:")
            for order in recent_orders:
                payments = Payment.query.filter_by(order_id=order.id).all()
                print(f"   {order.order_number}: {order.status} / {order.payment_status}")
                print(f"      Payments: {len(payments)}")
                for payment in payments:
                    print(f"         - {payment.status} (KSh {payment.amount})")
            
            # Check payment status distribution
            print(f"\n📊 Payment Status Distribution:")
            status_counts = db.session.query(
                Order.payment_status,
                db.func.count(Order.id)
            ).group_by(Order.payment_status).all()
            
            for status, count in status_counts:
                print(f"   {status}: {count}")
                
    except Exception as e:
        print(f"❌ Error checking payment flow: {str(e)}")

if __name__ == "__main__":
    print("🚀 E-commerce Payment Status Fix Script")
    print("=" * 50)
    
    # Check current state
    check_payment_flow()
    
    # Ask user if they want to proceed
    print(f"\n❓ Do you want to proceed with fixing payment status issues? (yes/no): ", end="")
    response = input().strip().lower()
    
    if response in ['yes', 'y']:
        success = fix_ecommerce_payment_status()
        if success:
            print("\n🎉 Payment status fix completed successfully!")
        else:
            print("\n❌ Payment status fix failed!")
    else:
        print("\nℹ️ Skipping payment status fix.") 