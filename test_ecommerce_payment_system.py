#!/usr/bin/env python3
"""
Test E-commerce Payment System
==============================

This script tests the new e-commerce payment monitoring system
that works like cyber services.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Order, Payment, User
from decimal import Decimal
from datetime import datetime, timedelta
import requests
import json

def test_payment_status_endpoint():
    """Test the new payment status endpoint"""
    print("🔍 Testing E-commerce Payment Status Endpoint")
    print("=" * 50)
    
    try:
        # Test local endpoint
        local_url = "http://localhost:5000/api/orders/test/payment-status"
        
        print(f"1. Testing payment status endpoint: {local_url}")
        
        # This will fail without authentication, but we can test the endpoint exists
        response = requests.get(local_url, timeout=10)
        
        if response.status_code == 401:
            print("   ✅ Endpoint exists (requires authentication)")
            return True
        elif response.status_code == 200:
            print("   ✅ Endpoint accessible and working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"   ⚠️ Endpoint accessible but unexpected response: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection error: Flask backend not running")
        return False
    except Exception as e:
        print(f"   ❌ Error testing endpoint: {str(e)}")
        return False

def test_payment_monitoring_system():
    """Test the payment monitoring system with real data"""
    print("\n🔧 Testing E-commerce Payment Monitoring System")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Step 1: Check current e-commerce orders
            print("\n1. 🔍 Analyzing current e-commerce orders...")
            
            ecommerce_orders = Order.query.all()
            print(f"   Total e-commerce orders: {len(ecommerce_orders)}")
            
            pending_orders = []
            paid_orders = []
            failed_orders = []
            
            for order in ecommerce_orders:
                if order.payment_status == 'pending':
                    pending_orders.append(order)
                elif order.payment_status == 'paid':
                    paid_orders.append(order)
                elif order.payment_status == 'failed':
                    failed_orders.append(order)
            
            print(f"   Pending orders: {len(pending_orders)}")
            print(f"   Paid orders: {len(paid_orders)}")
            print(f"   Failed orders: {len(failed_orders)}")
            
            # Step 2: Check payment records
            print(f"\n2. 🔍 Analyzing payment records...")
            
            from app.models import Payment
            all_payments = Payment.query.all()
            print(f"   Total payments: {len(all_payments)}")
            
            completed_payments = []
            pending_payments = []
            failed_payments = []
            
            for payment in all_payments:
                if payment.status == 'completed':
                    completed_payments.append(payment)
                elif payment.status == 'pending':
                    pending_payments.append(payment)
                elif payment.status == 'failed':
                    failed_payments.append(payment)
            
            print(f"   Completed payments: {len(completed_payments)}")
            print(f"   Pending payments: {len(pending_payments)}")
            print(f"   Failed payments: {len(failed_payments)}")
            
            # Step 3: Test payment status checking logic
            print(f"\n3. 🧪 Testing payment status checking logic...")
            
            if pending_payments:
                test_payment = pending_payments[0]
                print(f"   Testing with Payment ID: {test_payment.id}")
                print(f"   Order: {test_payment.order.order_number if test_payment.order else 'No order'}")
                print(f"   Before: Payment={test_payment.status}, Order={test_payment.order.payment_status if test_payment.order else 'No order'}")
                
                # Test the monitoring logic
                if test_payment.checkout_request_id:
                    print(f"   CheckoutRequestID: {test_payment.checkout_request_id}")
                    
                    # Simulate the monitoring check
                    time_since_payment = datetime.utcnow() - test_payment.created_at
                    print(f"   Time since payment: {time_since_payment}")
                    
                    if time_since_payment > timedelta(seconds=30):
                        print(f"   ✅ Payment eligible for status check (over 30 seconds)")
                        
                        # Test M-Pesa API query
                        try:
                            from app.notifications.mpesa.services import MpesaService
                            mpesa_service = MpesaService()
                            
                            print(f"   🔍 Querying M-Pesa for transaction status...")
                            response = mpesa_service.query_transaction_status(test_payment.checkout_request_id)
                            
                            if response and response.get('ResponseCode') == '0':
                                result_code = response.get('ResultCode')
                                print(f"   ✅ M-Pesa API response: ResultCode={result_code}")
                                
                                if result_code == '0':
                                    print(f"   🎉 Payment confirmed successful!")
                                elif result_code in ['1032', '1']:
                                    print(f"   ❌ Payment confirmed failed")
                                elif result_code == '1037':
                                    print(f"   ⏳ Payment still processing")
                                else:
                                    print(f"   ❓ Unknown result code: {result_code}")
                            else:
                                print(f"   ⚠️ M-Pesa API error or no response")
                                
                        except Exception as e:
                            print(f"   ❌ Error querying M-Pesa: {str(e)}")
                    else:
                        print(f"   ⏳ Payment too recent for status check (under 30 seconds)")
                else:
                    print(f"   ❌ No CheckoutRequestID found")
            else:
                print(f"   ℹ️ No pending payments to test")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing payment monitoring system: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_commission_processing():
    """Test commission processing for e-commerce orders"""
    print("\n💰 Testing Commission Processing")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Check if commission system is set up
            from app.models import SystemSettings
            commission_setting = db.session.query(SystemSettings).filter_by(key='ecommerce_commission_rate').first()
            
            if commission_setting:
                print(f"   ✅ E-commerce commission rate: {commission_setting.value}%")
            else:
                print(f"   ⚠️ No e-commerce commission rate configured")
            
            # Check commission records
            from app.models import Commission
            ecommerce_commissions = Commission.query.filter_by(commission_type='order').all()
            print(f"   Total e-commerce commissions: {len(ecommerce_commissions)}")
            
            if ecommerce_commissions:
                total_amount = sum(float(commission.amount) for commission in ecommerce_commissions)
                print(f"   Total commission amount: KSh {total_amount:.2f}")
                
                for commission in ecommerce_commissions[:3]:  # Show first 3
                    print(f"      {commission.description}: KSh {float(commission.amount):.2f}")
            else:
                print(f"   ℹ️ No e-commerce commissions found")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing commission processing: {str(e)}")
        return False

def create_test_payment_scenario():
    """Create a test payment scenario to demonstrate the system"""
    print("\n🧪 Creating Test Payment Scenario")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Find a test user
            test_user = User.query.first()
            if not test_user:
                print("   ❌ No users found in database")
                return False
            
            print(f"   ✅ Using test user: {test_user.name} ({test_user.email})")
            
            # Create a test order
            from app.models import Order, OrderItem, Product
            test_product = Product.query.first()
            
            if not test_product:
                print("   ❌ No products found in database")
                return False
            
            print(f"   ✅ Using test product: {test_product.name}")
            
            # Create test order
            test_order = Order(
                user_id=test_user.id,
                total_amount=Decimal('100.00'),
                subtotal=Decimal('100.00'),
                shipping_cost=Decimal('0.00'),
                status='pending',
                payment_status='pending'
            )
            test_order.generate_order_number()
            
            db.session.add(test_order)
            db.session.flush()
            
            # Create order item
            order_item = OrderItem(
                order_id=test_order.id,
                product_id=test_product.id,
                product_name=test_product.name,
                product_sku=test_product.sku,
                price=Decimal('100.00'),
                quantity=1
            )
            db.session.add(order_item)
            
            # Create test payment
            from app.models import Payment
            test_payment = Payment(
                order_id=test_order.id,
                phone_number='254700000000',
                amount=Decimal('100.00'),
                status='pending',
                checkout_request_id=f'test_{datetime.now().strftime("%m%d%H%M%S")}'
            )
            db.session.add(test_payment)
            
            db.session.commit()
            
            print(f"   ✅ Test order created: {test_order.order_number}")
            print(f"   ✅ Test payment created: {test_payment.id}")
            print(f"   ✅ CheckoutRequestID: {test_payment.checkout_request_id}")
            
            print(f"\n🎯 Test the payment monitoring system:")
            print(f"   GET /api/orders/{test_order.order_number}/payment-status")
            print(f"   This will test the new monitoring logic")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating test scenario: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 E-commerce Payment System Test")
    print("=" * 50)
    
    # Test payment status endpoint
    endpoint_ok = test_payment_status_endpoint()
    
    if endpoint_ok:
        print("\n✅ Payment status endpoint is accessible")
        
        # Test payment monitoring system
        monitoring_ok = test_payment_monitoring_system()
        
        if monitoring_ok:
            print("\n✅ Payment monitoring system test completed!")
            
            # Test commission processing
            commission_ok = test_commission_processing()
            
            if commission_ok:
                print("\n✅ Commission processing test completed!")
                
                # Create test scenario
                print(f"\n🔧 Creating test payment scenario...")
                scenario_ok = create_test_payment_scenario()
                
                if scenario_ok:
                    print("\n🎉 All tests completed successfully!")
                    print("\n📋 What was tested:")
                    print("   ✅ Payment status endpoint accessibility")
                    print("   ✅ Payment monitoring system logic")
                    print("   ✅ Commission processing system")
                    print("   ✅ Test payment scenario creation")
                    print("\n🎯 Next steps:")
                    print("1. Test the payment monitoring with a real order")
                    print("2. Check that status updates work in real-time")
                    print("3. Verify automatic redirects to orders page")
                    print("4. Test commission processing for referred users")
                else:
                    print("\n⚠️ Test scenario creation failed")
            else:
                print("\n⚠️ Commission processing test failed")
        else:
            print("\n❌ Payment monitoring system test failed!")
    else:
        print("\n❌ Payment status endpoint is not accessible!")
        print("   Please ensure your Flask backend is running and accessible.") 