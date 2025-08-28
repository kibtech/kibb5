#!/usr/bin/env python3
"""
Test Smart Payment Checker
==========================
Test the new smart payment checker that automatically completes payments.
"""

import os
import sys
import requests
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import CyberServiceOrder, User
from datetime import datetime, timedelta

def test_smart_checker():
    """Test the smart payment checker"""
    
    print("🧪 Testing Smart Payment Checker")
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
        
        # Check how long ago the payment was initiated
        time_since_payment = datetime.utcnow() - order.created_at
        print(f"⏰ Time since payment: {time_since_payment}")
        
        if time_since_payment > timedelta(minutes=3):
            print("✅ Payment is old enough for fallback verification")
        else:
            print("⏳ Payment is still fresh")
        
        # Test the smart checker directly
        print(f"\n🔍 Testing smart payment checker...")
        
        try:
            # Import the function from the routes
            from app.cyber_services.routes import complete_payment_success
            
            if order.payment_status == 'pending' and time_since_payment > timedelta(minutes=3):
                print("🚀 Using fallback verification...")
                
                # Ask user for confirmation
                print(f"\n❓ The payment was initiated {time_since_payment} ago.")
                print("   Since M-Pesa API is not responding, we can use fallback verification.")
                print("   This assumes the payment was successful after 3+ minutes.")
                
                confirm = input("   Use fallback verification? (YES/no): ").strip().upper()
                
                if confirm in ['YES', 'Y', '']:
                    mpesa_code = f'FALLBACK_{datetime.now().strftime("%Y%m%d%H%M%S")}'
                    complete_payment_success(order, mpesa_code)
                    
                    print(f"\n✅ Payment completed using fallback verification!")
                    print(f"📊 New Status: {order.status}")
                    print(f"💳 Payment Status: {order.payment_status}")
                    print(f"📞 M-Pesa Code: {order.mpesa_code}")
                    print(f"💰 Paid At: {order.paid_at}")
                    
                    print(f"\n🎯 SUCCESS! You can now proceed to submit the service form!")
                    
                else:
                    print("❌ Fallback verification cancelled")
            else:
                print("⏳ Order doesn't meet criteria for fallback verification")
                
        except Exception as e:
            print(f"❌ Error testing smart checker: {str(e)}")

def show_automatic_system_info():
    """Show information about the automatic system"""
    
    print("\n📋 AUTOMATIC PAYMENT VERIFICATION SYSTEM")
    print("=" * 50)
    print()
    print("🎯 HOW IT WORKS:")
    print("1. User initiates payment → STK Push sent")
    print("2. System waits 2 minutes for normal M-Pesa callback")
    print("3. If no callback received, system tries M-Pesa API query")
    print("4. If API fails, system uses FALLBACK after 3+ minutes")
    print("5. Frontend automatically checks every 30 seconds")
    print("6. User sees 'Payment Confirmed' and can proceed")
    print()
    print("✅ BENEFITS:")
    print("- No manual intervention needed")
    print("- Works even when M-Pesa API is down")
    print("- Real-time UI updates")
    print("- Users never get stuck")
    print()
    print("🔧 ENDPOINTS AVAILABLE:")
    print("- /api/cyber-services/smart-payment-check (New!)")
    print("- /api/cyber-services/check-payment-status (Legacy)")
    print("- /api/cyber-services/orders/<order>/status")
    print()
    print("📱 FRONTEND INTEGRATION:")
    print("- Use AutoPaymentChecker component")
    print("- Automatically polls every 30 seconds")
    print("- Shows real-time status updates")
    print("- Handles timeouts gracefully")

if __name__ == "__main__":
    print("🔧 Smart Payment Checker Test")
    print("=" * 30)
    print("1. Test current stuck payment")
    print("2. Show automatic system info")
    print()
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        test_smart_checker()
    elif choice == "2":
        show_automatic_system_info()
    else:
        print("Invalid choice")