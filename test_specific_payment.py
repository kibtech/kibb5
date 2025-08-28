#!/usr/bin/env python3
"""
Test Specific Payment Status
===========================
Test the specific payment that's stuck in pending status.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import db, CyberServiceOrder
from app.notifications.mpesa.services import MpesaService
from datetime import datetime

def test_specific_payment():
    """Test the specific payment that's stuck"""
    
    print("🧪 Testing Specific Payment Status")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Get the specific order
        order = CyberServiceOrder.query.filter_by(order_number="CS202508080919512").first()
        
        if not order:
            print("❌ Order not found")
            return
        
        print(f"📋 Testing Order: {order.order_number}")
        print(f"💰 Amount: KSh {order.amount}")
        print(f"📊 Current Status: {order.status}")
        print(f"💳 Payment Status: {order.payment_status}")
        print(f"🔑 Payment ID: {order.payment_id}")
        print(f"📅 Created: {order.created_at}")
        
        if not order.payment_id:
            print("❌ No payment ID found - payment was never initiated")
            return
        
        print(f"\n🔍 Querying M-Pesa for payment status...")
        
        try:
            mpesa_service = MpesaService()
            response = mpesa_service.query_transaction_status(order.payment_id)
            
            print(f"📞 M-Pesa Response:")
            print(f"   Response Code: {response.get('ResponseCode')}")
            print(f"   Response Description: {response.get('ResponseDescription')}")
            
            if response.get('ResponseCode') == '0':
                result_code = response.get('ResultCode')
                result_desc = response.get('ResultDesc')
                
                print(f"   Result Code: {result_code}")
                print(f"   Result Description: {result_desc}")
                
                if result_code == '0':
                    print("\n✅ PAYMENT WAS SUCCESSFUL!")
                    print("   The payment went through but the callback wasn't processed.")
                    
                    # Get M-Pesa receipt number if available
                    mpesa_receipt = response.get('MpesaReceiptNumber')
                    if mpesa_receipt:
                        print(f"   M-Pesa Receipt: {mpesa_receipt}")
                    
                    # Ask if user wants to update the order
                    print("\n❓ Would you like to update the order status now?")
                    confirm = input("Type 'YES' to update: ").strip().upper()
                    
                    if confirm == 'YES':
                        # Update the order
                        order.payment_status = 'completed'
                        order.status = 'paid'
                        order.mpesa_code = mpesa_receipt or f'MANUAL_{datetime.now().strftime("%Y%m%d%H%M%S")}'
                        order.paid_at = datetime.utcnow()
                        order.updated_at = datetime.utcnow()
                        
                        # Process commission if needed
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
                        
                        db.session.commit()
                        print("\n✅ Order updated successfully!")
                        print("🎯 You can now proceed to submit the service form!")
                    
                elif result_code == '1032':
                    print("\n❌ Payment was cancelled by user")
                    
                elif result_code == '1':
                    print("\n❌ Payment failed - insufficient funds")
                    
                else:
                    print(f"\n⏳ Payment still pending (Result Code: {result_code})")
                    print("   This might mean the STK push is still waiting for user action")
                    
            else:
                print(f"\n⚠️ Could not query payment status")
                print(f"   Error: {response.get('ResponseDescription', 'Unknown error')}")
                
        except Exception as e:
            print(f"\n❌ Error querying payment status: {str(e)}")

if __name__ == "__main__":
    test_specific_payment()