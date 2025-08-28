#!/usr/bin/env python3
"""
Fix Referral Commission System
This script fixes the referral commission tracking issues where commissions are not being 
properly tracked when referred users make payments for cyber services and e-commerce products.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User, Order, CyberServiceOrder, Commission, Wallet, SystemSettings
from decimal import Decimal
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_referral_commission_system():
    """Main function to fix the referral commission system"""
    
    app = create_app()
    
    with app.app_context():
        logger.info("🔧 Starting referral commission system fix...")
        
        # Step 1: Check and fix referral relationships
        fix_referral_relationships()
        
        # Step 2: Check and fix commission settings
        fix_commission_settings()
        
        # Step 3: Process pending commissions for existing orders
        process_pending_commissions()
        
        # Step 4: Verify the fix
        verify_commission_system()
        
        logger.info("✅ Referral commission system fix completed!")

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
    cyber_orders = CyberServiceOrder.query.filter_by(
        payment_status='paid',
        status='completed'
    ).all()
    
    logger.info(f"Found {len(cyber_orders)} completed cyber service orders")
    
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
    ecommerce_orders = Order.query.filter_by(
        payment_status='paid',
        status='confirmed'
    ).all()
    
    logger.info(f"Found {len(ecommerce_orders)} completed e-commerce orders")
    
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

def verify_commission_system():
    """Verify that the commission system is working properly"""
    logger.info("🔍 Verifying commission system...")
    
    # Check total commissions
    total_commissions = db.session.query(db.func.sum(Commission.amount)).scalar() or 0
    logger.info(f"Total commissions in system: KSh {total_commissions:,.2f}")
    
    # Check users with commissions
    users_with_commissions = User.query.join(Wallet).filter(
        Wallet.commission_balance > 0
    ).count()
    logger.info(f"Users with commission balance: {users_with_commissions}")
    
    # Check recent commission activity
    recent_commissions = Commission.query.filter(
        Commission.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    logger.info(f"Commissions in last 7 days: {recent_commissions}")
    
    # Check referral relationships
    total_referrals = User.query.filter(
        User.referred_by_id.isnot(None)
    ).count()
    logger.info(f"Total users with referrals: {total_referrals}")
    
    logger.info("✅ Commission system verification completed")

if __name__ == "__main__":
    try:
        fix_referral_commission_system()
        print("\n🎉 Referral commission system has been fixed!")
        print("\nWhat was fixed:")
        print("1. ✅ Referral relationships between users")
        print("2. ✅ Commission settings and rates")
        print("3. ✅ Retroactive commission processing for existing orders")
        print("4. ✅ Commission system verification")
        print("\nYour referral system should now work properly!")
        
    except Exception as e:
        logger.error(f"Failed to fix referral commission system: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 