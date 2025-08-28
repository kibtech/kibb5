#!/usr/bin/env python3
"""
Fix stuck cyber service payment by manually completing it
"""

from app import create_app
from app.models import db, CyberServiceOrder, User, Commission, SystemSettings
from app.notifications.mpesa.services import MpesaService
from datetime import datetime
from decimal import Decimal

def manually_complete_payment(order_number, mpesa_code=None):
    """Manually complete a stuck payment"""
    app = create_app()
    with app.app_context():
        order = db.session.query(CyberServiceOrder).filter_by(order_number=order_number).first()
        
        if not order:
            print(f"❌ Order {order_number} not found")
            return False
            
        if order.payment_status == 'completed':
            print(f"✅ Order {order_number} is already completed")
            return True
            
        print(f"🔧 Manually completing payment for order {order_number}")
        
        # Generate M-Pesa code if not provided
        if not mpesa_code:
            mpesa_code = f"MANUAL{datetime.now().strftime('%m%d%H%M')}"
        
        # Update order status
        order.payment_status = 'completed'
        order.status = 'paid'
        order.mpesa_code = mpesa_code
        order.paid_at = datetime.utcnow()
        order.updated_at = datetime.utcnow()
        
        # Update progress tracking
        order.update_progress()
        
        # Process commission if user was referred
        user_obj = db.session.get(User, order.user_id)
        if user_obj and user_obj.referred_by_id:
            commission_setting = db.session.query(SystemSettings).filter_by(key='cyber_services_commission_rate').first()
            commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.20
            
            commission_amount = Decimal(str(float(order.amount) * commission_rate))
            
            # Create commission record
            commission = Commission(
                referrer_id=user_obj.referred_by_id,
                order_id=order.id,
                amount=commission_amount,
                commission_type='order',
                description=f'Commission from cyber service order {order.order_number} (manually completed)'
            )
            db.session.add(commission)
            
            # Update referrer's wallet
            referrer = db.session.get(User, user_obj.referred_by_id)
            if referrer and referrer.wallet:
                referrer.wallet.add_commission(commission_amount)
                print(f"💰 Commission of KSh {commission_amount} added to referrer's wallet")
        
        db.session.commit()
        print(f"✅ Payment completed successfully for order {order_number}")
        print(f"   Status: {order.status}")
        print(f"   Payment Status: {order.payment_status}")
        print(f"   M-Pesa Code: {order.mpesa_code}")
        
        return True

def test_mpesa_query(order_number):
    """Test M-Pesa transaction status query"""
    app = create_app()
    with app.app_context():
        order = db.session.query(CyberServiceOrder).filter_by(order_number=order_number).first()
        
        if not order or not order.payment_id:
            print(f"❌ Order {order_number} not found or no payment ID")
            return
            
        print(f"🔍 Testing M-Pesa query for payment ID: {order.payment_id}")
        
        try:
            mpesa_service = MpesaService()
            response = mpesa_service.query_transaction_status(order.payment_id)
            
            print(f"📱 M-Pesa API Response:")
            print(f"   ResponseCode: {response.get('ResponseCode')}")
            print(f"   ResultCode: {response.get('ResultCode')}")
            print(f"   ResultDesc: {response.get('ResultDesc')}")
            
            if response.get('ResponseCode') == '0':
                result_code = response.get('ResultCode')
                if result_code == '0':
                    print("✅ Payment successful according to M-Pesa!")
                    print("🔧 The callback should have updated this automatically")
                elif result_code in ['1032', '1']:
                    print("❌ Payment failed/cancelled according to M-Pesa")
                elif result_code == '1037':
                    print("⏳ Payment still in progress according to M-Pesa")
                else:
                    print(f"❓ Unknown result code: {result_code}")
            else:
                print("❌ Failed to query M-Pesa status")
                
        except Exception as e:
            print(f"❌ Error querying M-Pesa: {str(e)}")

def main():
    # Test M-Pesa query first
    print("=== Testing M-Pesa Status Query ===")
    test_mpesa_query('CS202508141250213')
    
    print("\n=== Manual Payment Completion ===")
    # Manually complete the stuck payment
    manually_complete_payment('CS202508141250213', 'MANUAL0814')
    
    print("\n=== Checking Other Stuck Payments ===")
    app = create_app()
    with app.app_context():
        stuck_orders = db.session.query(CyberServiceOrder).filter_by(
            status='payment_initiated',
            payment_status='pending'
        ).all()
        
        print(f"Found {len(stuck_orders)} stuck payments:")
        for order in stuck_orders:
            time_diff = datetime.utcnow() - order.created_at
            minutes = time_diff.total_seconds() / 60
            print(f"  {order.order_number}: {minutes:.1f} minutes old")
            
            # Auto-complete payments older than 5 minutes
            if minutes > 5:
                print(f"    🔧 Auto-completing (older than 5 minutes)")
                manually_complete_payment(order.order_number)
            else:
                print(f"    ⏳ Still recent, leaving for M-Pesa callback")

if __name__ == "__main__":
    main()