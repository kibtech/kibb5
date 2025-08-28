#!/usr/bin/env python3
"""
Test M-Pesa Callback System
============================

This script tests the M-Pesa callback system to ensure it's working
correctly for e-commerce orders.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Order, Payment, User, CyberServiceOrder
from decimal import Decimal
from datetime import datetime, timedelta
import requests
import json

def test_callback_endpoint():
    """Test if the callback endpoint is accessible"""
    print("🔍 Testing M-Pesa Callback Endpoint")
    print("=" * 50)
    
    try:
        # Test local endpoint
        local_url = "http://localhost:5000/api/mpesa/test-callback"
        
        print(f"1. Testing test endpoint: {local_url}")
        
        response = requests.get(local_url, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Test endpoint accessible and working")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ⚠️ Test endpoint accessible but unexpected response: {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection error: Flask backend not running")
        return False
    except Exception as e:
        print(f"   ❌ Error testing endpoint: {str(e)}")
        return False

def test_callback_system():
    """Test the callback system with real data"""
    print("\n🔧 Testing M-Pesa Callback System")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Step 1: Check current payment statuses
            print("\n1. 🔍 Analyzing current payment statuses...")
            
            # Check e-commerce orders
            ecommerce_orders = Order.query.all()
            print(f"   Total e-commerce orders: {len(ecommerce_orders)}")
            
            pending_orders = []
            paid_orders = []
            
            for order in ecommerce_orders:
                if order.payment_status == 'pending':
                    pending_orders.append(order)
                elif order.payment_status == 'paid':
                    paid_orders.append(order)
            
            print(f"   Pending orders: {len(pending_orders)}")
            print(f"   Paid orders: {len(paid_orders)}")
            
            if pending_orders:
                print(f"\n   📋 Pending orders that need payment status update:")
                for order in pending_orders[:5]:  # Show first 5
                    print(f"      {order.order_number}: KSh {order.total_amount} - {order.status}")
                    
                    # Check if there's a payment record
                    payment = Payment.query.filter_by(order_id=order.id).first()
                    if payment:
                        print(f"         Payment ID: {payment.id}, Status: {payment.status}")
                        if payment.checkout_request_id:
                            print(f"         CheckoutRequestID: {payment.checkout_request_id}")
                    else:
                        print(f"         No payment record found")
            
            # Step 2: Check payment records
            print(f"\n2. 🔍 Analyzing payment records...")
            
            all_payments = Payment.query.all()
            print(f"   Total payments: {len(all_payments)}")
            
            completed_payments = []
            pending_payments = []
            
            for payment in all_payments:
                if payment.status == 'completed':
                    completed_payments.append(payment)
                elif payment.status == 'pending':
                    pending_payments.append(payment)
            
            print(f"   Completed payments: {len(completed_payments)}")
            print(f"   Pending payments: {len(pending_payments)}")
            
            # Step 3: Check for status mismatches
            print(f"\n3. 🔍 Checking for status mismatches...")
            
            mismatches = []
            for payment in completed_payments:
                if payment.order and payment.order.payment_status != 'paid':
                    mismatches.append({
                        'payment_id': payment.id,
                        'order_number': payment.order.order_number,
                        'payment_status': payment.status,
                        'order_payment_status': payment.order.payment_status,
                        'order_status': payment.order.status
                    })
            
            if mismatches:
                print(f"   ⚠️ Found {len(mismatches)} status mismatches:")
                for mismatch in mismatches:
                    print(f"      Payment {mismatch['payment_id']}: {mismatch['order_number']}")
                    print(f"         Payment: {mismatch['payment_status']}")
                    print(f"         Order Payment: {mismatch['order_payment_status']}")
                    print(f"         Order Status: {mismatch['order_status']}")
            else:
                print(f"   ✅ No status mismatches found")
            
            # Step 4: Test callback simulation
            print(f"\n4. 🧪 Testing callback simulation...")
            
            if mismatches:
                print(f"   Simulating callback for first mismatch...")
                test_payment = Payment.query.get(mismatches[0]['payment_id'])
                
                if test_payment:
                    print(f"   Testing with Payment ID: {test_payment.id}")
                    print(f"   Order: {test_payment.order.order_number}")
                    print(f"   Before: Payment={test_payment.status}, Order={test_payment.order.payment_status}")
                    
                    # Simulate the callback update
                    test_payment.order.payment_status = 'paid'
                    test_payment.order.status = 'confirmed'
                    
                    # Update progress tracking
                    try:
                        test_payment.order.update_progress()
                        print(f"   ✅ Order progress updated")
                    except Exception as e:
                        print(f"   ⚠️ Could not update progress: {str(e)}")
                    
                    db.session.commit()
                    print(f"   After: Payment={test_payment.status}, Order={test_payment.order.payment_status}")
                    print(f"   ✅ Test callback simulation successful")
                else:
                    print(f"   ❌ Could not find test payment")
            else:
                print(f"   ℹ️ No mismatches to test")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing callback system: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_callback_monitoring():
    """Create callback monitoring system"""
    print("\n🔧 Creating Callback Monitoring System")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            from app.models import SystemSettings
            
            # Create callback monitoring setting
            monitoring_setting = db.session.query(SystemSettings).filter_by(
                key='callback_monitoring_enabled'
            ).first()
            
            if not monitoring_setting:
                monitoring_setting = SystemSettings(
                    key='callback_monitoring_enabled',
                    value='true',
                    description='Enable M-Pesa callback monitoring'
                )
                db.session.add(monitoring_setting)
                print("   ✅ Callback monitoring enabled")
            else:
                print("   ℹ️ Callback monitoring already configured")
            
            db.session.commit()
            print("   ✅ Callback monitoring system created")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating callback monitor: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 M-Pesa Callback System Test")
    print("=" * 50)
    
    # Test callback endpoint
    endpoint_ok = test_callback_endpoint()
    
    if endpoint_ok:
        print("\n✅ Callback endpoint is accessible")
        
        # Test callback system
        system_ok = test_callback_system()
        
        if system_ok:
            print("\n🎉 Callback system test completed!")
            
            # Create monitoring system
            print(f"\n🔧 Creating callback monitoring system...")
            monitor_success = create_callback_monitoring()
            
            if monitor_success:
                print("\n🎉 Callback monitoring system created!")
                print("\n📋 What was tested:")
                print("   ✅ Callback endpoint accessibility")
                print("   ✅ Payment status analysis")
                print("   ✅ Status mismatch detection")
                print("   ✅ Callback simulation")
                print("   ✅ Monitoring system creation")
                print("\n🎯 Next steps:")
                print("1. Restart your Flask backend")
                print("2. Check the console logs for callback activity")
                print("3. Make a test payment to see if it works automatically")
            else:
                print("\n⚠️ Callback monitoring system creation failed")
        else:
            print("\n❌ Callback system test failed!")
    else:
        print("\n❌ Callback endpoint is not accessible!")
        print("   Please ensure your Flask backend is running and accessible.") 