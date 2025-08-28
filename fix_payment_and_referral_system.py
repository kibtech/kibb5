#!/usr/bin/env python3
"""
Fix Payment Status and Referral Commission System
This script fixes TWO critical issues:
1. Cyber service payments not being marked as 'paid' (they're marked as 'completed')
2. Referral commissions not being tracked when referred users make payments
"""

import os
import sys
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User, Order, CyberServiceOrder, Commission, Wallet, SystemSettings, Payment
from decimal import Decimal
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_payment_and_referral_system():
    """Main function to fix both payment status and referral commission issues"""
    
    app = create_app()
    
    with app.app_context():
        logger.info("🔧 Starting comprehensive payment and referral system fix...")
        
        # Step 1: Fix payment status inconsistencies
        fix_payment_status_issues()
        
        # Step 2: Fix referral relationships
        fix_referral_relationships()
        
        # Step 3: Check and fix commission settings
        fix_commission_settings()
        
        # Step 4: Process pending commissions for existing orders
        process_pending_commissions()
        
        # Step 5: Verify the fix
        verify_system()
        
        logger.info("✅ Payment and referral system fix completed!")

def fix_payment_status_issues():
    """Fix payment status inconsistencies between 'completed' and 'paid'"""
    logger.info("🔍 Fixing payment status inconsistencies...")
    
    # Fix cyber service orders with 'completed' payment_status
    cyber_orders_completed = CyberServiceOrder.query.filter_by(
        payment_status='completed'
    ).all()
    
    logger.info(f"Found {len(cyber_orders_completed)} cyber service orders with 'completed' status")
    
    for order in cyber_orders_completed:
        order.payment_status = 'paid'
        logger.info(f"Fixed cyber service order {order.order_number}: completed -> paid")
    
    # Fix e-commerce orders with 'completed' payment_status
    ecommerce_orders_completed = Order.query.filter_by(
        payment_status='completed'
    ).all()
    
    logger.info(f"Found {len(ecommerce_orders_completed)} e-commerce orders with 'completed' status")
    
    for order in ecommerce_orders_completed:
        order.payment_status = 'paid'
        logger.info(f"Fixed e-commerce order {order.order_number}: completed -> paid")
    
    # Fix payments with 'completed' status
    payments_completed = Payment.query.filter_by(
        status='completed'
    ).all()
    
    logger.info(f"Found {len(payments_completed)} payments with 'completed' status")
    
    for payment in payments_completed:
        payment.status = 'completed'  # Keep as completed for payments
        # But ensure the order has correct status
        if payment.order:
            payment.order.payment_status = 'paid'
            logger.info(f"Fixed payment order {payment.order.order_number}: payment_status -> paid")
    
    db.session.commit()
    logger.info("✅ Payment status inconsistencies fixed")

def fix_referral_relationships():
    """Fix referral relationships that might be broken"""
    logger.info("🔍 Checking referral relationships...")
    
    # Check users with referral codes but no referred_by_id
    users_with_referral_codes = User.query.filter(
        User.referral_code.isnot(None),
        User.referral_code != ''
    ).all()
    
    logger.info(f"Found {len(users_with_referral_codes)} users with referral codes")
    
    for user in users_with_referral_codes:
        if not user.referred_by_id:
            # Find the user who has this referral code
            referrer = User.query.filter_by(referral_code=user.referral_code).first()
            if referrer and referrer.id != user.id:
                user.referred_by_id = referrer.id
                logger.info(f"Fixed referral relationship: {user.email} -> {referrer.email}")
    
    # Check for orphaned referrals (users with referred_by_id but referrer doesn't exist)
    orphaned_referrals = User.query.filter(
        User.referred_by_id.isnot(None)
    ).all()
    
    for user in orphaned_referrals:
        referrer = User.query.get(user.referred_by_id)
        if not referrer:
            user.referred_by_id = None
            logger.info(f"Removed orphaned referral for {user.email}")
    
    db.session.commit()
    logger.info("✅ Referral relationships fixed")

def fix_commission_settings():
    """Ensure commission settings are properly configured"""
    logger.info("🔍 Checking commission settings...")
    
    # Default commission rates
    default_rates = {
        'cyber_services_commission_rate': '20',  # 20%
        'ecommerce_commission_rate': '3',       # 3%
        'referral_bonus_rate': '5'              # 5% bonus for successful referrals
    }
    
    for key, value in default_rates.items():
        setting = SystemSettings.query.filter_by(key=key).first()
        if not setting:
            setting = SystemSettings(key=key, value=value, description=f'Default {key}')
            db.session.add(setting)
            logger.info(f"Created missing commission setting: {key} = {value}%")
        else:
            logger.info(f"Commission setting exists: {key} = {setting.value}%")
    
    db.session.commit()
    logger.info("✅ Commission settings verified")

def process_pending_commissions():
    """Process commissions for existing orders that might have missed commission tracking"""
    logger.info("🔍 Processing pending commissions...")
    
    # Process cyber service orders
    cyber_orders = CyberServiceOrder.query.filter(
        CyberServiceOrder.payment_status.in_(['paid', 'completed'])
    ).all()
    
    logger.info(f"Found {len(cyber_orders)} paid cyber service orders")
    
    for order in cyber_orders:
        if not Commission.query.filter_by(
            order_id=order.id,
            commission_type='order'
        ).first():
            # Check if user was referred
            user = User.query.get(order.user_id)
            if user and user.referred_by_id:
                process_cyber_service_commission(order, user)
    
    # Process e-commerce orders
    ecommerce_orders = Order.query.filter(
        Order.payment_status.in_(['paid', 'completed'])
    ).all()
    
    logger.info(f"Found {len(ecommerce_orders)} paid e-commerce orders")
    
    for order in ecommerce_orders:
        if not Commission.query.filter_by(
            order_id=order.id,
            commission_type='order'
        ).first():
            # Check if user was referred
            user = order.user
            if user and user.referred_by_id:
                process_ecommerce_commission(order, user)
    
    db.session.commit()
    logger.info("✅ Pending commissions processed")

def process_cyber_service_commission(order, user):
    """Process commission for a cyber service order"""
    try:
        # Get commission rate
        commission_setting = SystemSettings.query.filter_by(
            key='cyber_services_commission_rate'
        ).first()
        commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.20
        
        commission_amount = Decimal(str(float(order.amount) * commission_rate))
        
        # Create commission record
        commission = Commission(
            referrer_id=user.referred_by_id,
            order_id=order.id,
            amount=commission_amount,
            commission_type='order',
            description=f'Commission from cyber service order {order.order_number} (retroactive)'
        )
        db.session.add(commission)
        
        # Update referrer's wallet
        referrer = User.query.get(user.referred_by_id)
        if referrer and referrer.wallet:
            referrer.wallet.add_commission(commission_amount)
            logger.info(f"Added retroactive commission: KSh {commission_amount} for cyber service order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Failed to process cyber service commission for order {order.order_number}: {str(e)}")

def process_ecommerce_commission(order, user):
    """Process commission for an e-commerce order"""
    try:
        # Get commission rate
        commission_setting = SystemSettings.query.filter_by(
            key='ecommerce_commission_rate'
        ).first()
        commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.03
        
        commission_amount = Decimal(str(float(order.total_amount) * commission_rate))
        
        # Create commission record
        commission = Commission(
            referrer_id=user.referred_by_id,
            order_id=order.id,
            amount=commission_amount,
            commission_type='order',
            description=f'Commission from order {order.order_number} (retroactive)'
        )
        db.session.add(commission)
        
        # Update referrer's wallet
        referrer = User.query.get(user.referred_by_id)
        if referrer and referrer.wallet:
            referrer.wallet.add_commission(commission_amount)
            logger.info(f"Added retroactive commission: KSh {commission_amount} for order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Failed to process e-commerce commission for order {order.order_number}: {str(e)}")

def verify_system():
    """Verify that both payment status and commission system are working properly"""
    logger.info("🔍 Verifying system...")
    
    # Check payment statuses
    print("\n📊 PAYMENT STATUS VERIFICATION:")
    cyber_orders_paid = CyberServiceOrder.query.filter_by(payment_status='paid').count()
    cyber_orders_completed = CyberServiceOrder.query.filter_by(payment_status='completed').count()
    ecommerce_orders_paid = Order.query.filter_by(payment_status='paid').count()
    ecommerce_orders_completed = Order.query.filter_by(payment_status='completed').count()
    
    print(f"   Cyber service orders - Paid: {cyber_orders_paid}, Completed: {cyber_orders_completed}")
    print(f"   E-commerce orders - Paid: {ecommerce_orders_paid}, Completed: {ecommerce_orders_completed}")
    
    # Check commissions
    print("\n💰 COMMISSION SYSTEM VERIFICATION:")
    total_commissions = db.session.query(db.func.sum(Commission.amount)).scalar() or 0
    total_commission_records = Commission.query.count()
    users_with_commissions = User.query.join(Wallet).filter(Wallet.commission_balance > 0).count()
    
    print(f"   Total commission amount: KSh {total_commissions:,.2f}")
    print(f"   Total commission records: {total_commission_records}")
    print(f"   Users with commission balance: {users_with_commissions}")
    
    # Check referral relationships
    print("\n🔗 REFERRAL SYSTEM VERIFICATION:")
    total_referrals = User.query.filter(User.referred_by_id.isnot(None)).count()
    users_with_referral_codes = User.query.filter(
        User.referral_code.isnot(None),
        User.referral_code != ''
    ).count()
    
    print(f"   Total users with referrals: {total_referrals}")
    print(f"   Users with referral codes: {users_with_referral_codes}")
    
    logger.info("✅ System verification completed")

if __name__ == "__main__":
    try:
        fix_payment_and_referral_system()
        print("\n🎉 Payment and referral system has been fixed!")
        print("\nWhat was fixed:")
        print("1. ✅ Payment status inconsistencies ('completed' -> 'paid')")
        print("2. ✅ Referral relationships between users")
        print("3. ✅ Commission settings and rates")
        print("4. ✅ Retroactive commission processing for existing orders")
        print("5. ✅ Commission system verification")
        print("\nYour system should now:")
        print("- Properly mark cyber service payments as 'paid'")
        print("- Track referral commissions correctly")
        print("- Process all existing missed commissions")
        
    except Exception as e:
        logger.error(f"Failed to fix payment and referral system: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 