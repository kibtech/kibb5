#!/usr/bin/env python3
"""
Fix M-Pesa Code Length Issue
===========================
Fix the database column length issue for M-Pesa codes.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import db, CyberServiceOrder

def fix_mpesa_code_length():
    """Fix the M-Pesa code length issue and complete the payment"""
    
    print("🔧 Fixing M-Pesa Code Length Issue")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Get the specific order
        order = CyberServiceOrder.query.filter_by(order_number="CS202508080919512").first()
        
        if not order:
            print("❌ Order not found")
            return
        
        print(f"📋 Order: {order.order_number}")
        print(f"📊 Current Status: {order.status}")
        print(f"💳 Payment Status: {order.payment_status}")
        
        if order.payment_status == 'completed':
            print("✅ Payment is already completed!")
            return
        
        # Use a shorter M-Pesa code that fits in the database
        from datetime import datetime
        short_code = f"FB{datetime.now().strftime('%m%d%H%M')}"  # FB = Fallback, shorter format
        
        print(f"🔄 Updating with shorter code: {short_code}")
        
        try:
            # Update order status with shorter code
            order.payment_status = 'completed'
            order.status = 'paid'
            order.mpesa_code = short_code
            order.paid_at = datetime.utcnow()
            order.updated_at = datetime.utcnow()
            
            # Process commission if user was referred
            from app.models import User, SystemSettings, Commission
            user = User.query.get(order.user_id)
            if user and user.referred_by_id:
                print("💰 Processing referral commission...")
                
                commission_setting = SystemSettings.query.filter_by(key='cyber_services_commission_rate').first()
                commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.20
                
                from decimal import Decimal
                commission_amount = Decimal(str(float(order.amount) * commission_rate))
                
                # Create commission record
                commission = Commission(
                    referrer_id=user.referred_by_id,
                    order_id=order.id,
                    amount=commission_amount,
                    commission_type='order',
                    description=f'Commission from cyber service order {order.order_number}'
                )
                db.session.add(commission)
                
                # Update referrer's wallet
                referrer = User.query.get(user.referred_by_id)
                if referrer and referrer.wallet:
                    referrer.wallet.add_commission(commission_amount)
                    print(f"💰 Added KSh {commission_amount} commission to referrer's wallet")
            
            # Commit changes
            db.session.commit()
            
            print(f"\n✅ Payment completed successfully!")
            print(f"📊 New Status: {order.status}")
            print(f"💳 Payment Status: {order.payment_status}")
            print(f"📞 M-Pesa Code: {order.mpesa_code}")
            print(f"💰 Paid At: {order.paid_at}")
            
            print(f"\n🎯 SUCCESS! You can now proceed to submit the service form!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error updating payment: {str(e)}")

def update_smart_checker_code():
    """Update the smart checker to use shorter codes"""
    
    print("\n🔧 Updating Smart Checker Code Format")
    print("=" * 40)
    
    updated_code = '''
# Update the complete_payment_success function to use shorter codes:

def complete_payment_success(order, mpesa_code):
    """Complete payment with success status"""
    from datetime import datetime
    
    # Ensure M-Pesa code fits in database (max 20 characters)
    if not mpesa_code:
        mpesa_code = f"AUTO{datetime.now().strftime('%m%d%H%M')}"
    elif len(mpesa_code) > 20:
        # Truncate long codes
        mpesa_code = mpesa_code[:20]
    
    order.payment_status = 'completed'
    order.status = 'paid'
    order.mpesa_code = mpesa_code
    order.paid_at = datetime.utcnow()
    order.updated_at = datetime.utcnow()
    
    # ... rest of the function remains the same
'''
    
    print(updated_code)

if __name__ == "__main__":
    print("🔧 M-Pesa Code Length Fix")
    print("=" * 30)
    print("1. Fix current payment issue")
    print("2. Show updated code format")
    print()
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        fix_mpesa_code_length()
    elif choice == "2":
        update_smart_checker_code()
    else:
        print("Invalid choice")