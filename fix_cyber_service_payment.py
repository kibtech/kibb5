#!/usr/bin/env python3
"""
Fix Cyber Service Payment
=========================
Manually complete a cyber service payment that was successful but not processed.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import db, CyberServiceOrder, User, Commission
from datetime import datetime
from decimal import Decimal

def fix_cyber_service_payment():
    """Manually complete cyber service payment"""
    
    print("🔧 Fixing Cyber Service Payment")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Get the specific order that needs to be fixed
        order_number = "CS202508080919512"  # The order with payment_initiated status
        
        order = CyberServiceOrder.query.filter_by(order_number=order_number).first()
        
        if not order:
            print(f"❌ Order {order_number} not found")
            return
        
        print(f"📋 Found Order: {order.order_number}")
        print(f"👤 Customer: {order.customer_name}")
        print(f"💰 Amount: KSh {order.amount}")
        print(f"📊 Current Status: {order.status}")
        print(f"💳 Current Payment Status: {order.payment_status}")
        print(f"🔑 Payment ID: {order.payment_id}")
        
        # Ask for confirmation
        print("\n❓ Did you successfully complete the M-Pesa payment on your phone?")
        print("   If yes, this script will mark the payment as completed.")
        print("   If no, please complete the payment first.")
        
        confirm = input("\nType 'YES' to confirm payment was successful: ").strip().upper()
        
        if confirm != 'YES':
            print("❌ Operation cancelled. Please complete the payment first.")
            return
        
        # Ask for M-Pesa receipt number (optional but recommended)
        mpesa_code = input("\nEnter M-Pesa receipt number (or press Enter to skip): ").strip()
        if not mpesa_code:
            mpesa_code = f"MANUAL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        print(f"\n🔄 Updating payment status...")
        
        # Update order status
        order.payment_status = 'completed'
        order.status = 'paid'
        order.mpesa_code = mpesa_code
        order.paid_at = datetime.utcnow()
        order.updated_at = datetime.utcnow()
        
        # Process commission if user was referred (20% for cyber services)
        user = User.query.get(order.user_id)
        if user and user.referred_by_id:
            print(f"👥 Processing referral commission...")
            
            from app.models import SystemSettings
            commission_setting = SystemSettings.query.filter_by(key='cyber_services_commission_rate').first()
            commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.20  # 20% default
            
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
                
                # Send commission notification email
                try:
                    from app.services.email_service import get_email_service
                    email_service = get_email_service()
                    
                    # Prepare order details for email
                    order_details = {
                        'order_number': order.order_number,
                        'total_amount': float(order.amount),
                        'created_at': order.created_at.strftime('%B %d, %Y at %I:%M %p'),
                        'service_name': order.service.name if order.service else 'Cyber Service'
                    }
                    
                    # Send commission notification
                    email_service.send_commission_notification(
                        to_email=referrer.email,
                        referrer_name=referrer.name,
                        commission_amount=float(commission_amount),
                        order_details=order_details,
                        referred_user_name=user.name
                    )
                    
                    print(f"📧 Commission notification email sent to {referrer.email}")
                    
                except Exception as e:
                    print(f"⚠️ Failed to send commission notification email: {str(e)}")
        
        # Commit changes
        db.session.commit()
        
        print(f"\n✅ Payment completed successfully!")
        print(f"📊 New Status: {order.status}")
        print(f"💳 New Payment Status: {order.payment_status}")
        print(f"📞 M-Pesa Code: {order.mpesa_code}")
        print(f"💰 Paid At: {order.paid_at}")
        
        print(f"\n🎯 You can now proceed to submit the service form!")
        print(f"   Order Number: {order.order_number}")

if __name__ == "__main__":
    fix_cyber_service_payment()