#!/usr/bin/env python3
"""
Test Automatic Payment Verification
==================================
Test the automatic payment verification system for cyber services.
"""

import os
import sys
import requests
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import CyberServiceOrder

def test_payment_verification():
    """Test the automatic payment verification system"""
    
    print("🧪 Testing Automatic Payment Verification")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Check if we have any pending orders
        pending_orders = CyberServiceOrder.query.filter(
            CyberServiceOrder.status == 'payment_initiated',
            CyberServiceOrder.payment_status == 'pending',
            CyberServiceOrder.payment_id.isnot(None)
        ).all()
        
        if not pending_orders:
            print("❌ No pending orders found to test")
            return
        
        print(f"📋 Found {len(pending_orders)} pending orders:")
        
        for order in pending_orders:
            print(f"   - Order: {order.order_number}")
            print(f"     Payment ID: {order.payment_id}")
            print(f"     Amount: KSh {order.amount}")
            print(f"     User: {order.customer_name}")
        
        print("\n🔧 Testing payment verification endpoint...")
        
        # Test the endpoint (you would need to get a JWT token first)
        # For now, let's just test the M-Pesa query directly
        from app.notifications.mpesa.services import MpesaService
        
        mpesa_service = MpesaService()
        
        for order in pending_orders:
            print(f"\n🔍 Testing order: {order.order_number}")
            
            try:
                response = mpesa_service.query_transaction_status(order.payment_id)
                print(f"   M-Pesa Response: {json.dumps(response, indent=2)}")
                
                if response and response.get('ResponseCode') == '0':
                    result_code = response.get('ResultCode')
                    
                    if result_code == '0':
                        print("   ✅ Payment is successful!")
                    elif result_code == '1032':
                        print("   ❌ Payment was cancelled by user")
                    elif result_code == '1':
                        print("   ❌ Payment failed - insufficient funds")
                    else:
                        print(f"   ⏳ Payment still pending (Result Code: {result_code})")
                else:
                    print("   ⚠️ Could not query payment status")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")

def show_integration_guide():
    """Show how to integrate automatic payment checking in the frontend"""
    
    print("\n📝 Frontend Integration Guide")
    print("=" * 50)
    
    integration_code = '''
// Add this to your cyber service payment flow (JavaScript/React)

// After initiating payment, start polling for payment status
const checkPaymentStatus = async () => {
    try {
        const response = await fetch('/api/cyber-services/check-payment-status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.updated_orders.length > 0) {
            // Payment was successful! Refresh the order status
            console.log('Payment verified:', data.updated_orders);
            
            // Redirect to form submission or show success message
            window.location.reload(); // or update state
        }
        
    } catch (error) {
        console.error('Error checking payment status:', error);
    }
};

// Start checking payment status every 10 seconds after payment initiation
const startPaymentStatusCheck = () => {
    const interval = setInterval(() => {
        checkPaymentStatus();
    }, 10000); // Check every 10 seconds
    
    // Stop checking after 5 minutes (30 attempts)
    setTimeout(() => {
        clearInterval(interval);
    }, 300000);
    
    return interval;
};

// Usage in your payment component:
// After STK push is initiated:
const paymentInterval = startPaymentStatusCheck();

// You can also add a manual "Check Payment Status" button:
<button onClick={checkPaymentStatus}>
    Check Payment Status
</button>
'''
    
    print(integration_code)

if __name__ == "__main__":
    print("🔧 Automatic Payment Verification Test")
    print("=" * 40)
    print("1. Test payment verification")
    print("2. Show frontend integration guide")
    print()
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        test_payment_verification()
    elif choice == "2":
        show_integration_guide()
    else:
        print("Invalid choice")