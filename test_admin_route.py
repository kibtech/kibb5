#!/usr/bin/env python3
"""
Test script to test the admin route directly
"""

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import CyberServiceOrder, Order, AdminUser

def test_admin_route():
    """Test the admin route logic directly"""
    app = create_app()
    
    with app.app_context():
        print("🔍 Testing admin route logic directly...")
        
        # Test 1: Check if we can query orders directly
        print("\n📊 Test 1: Direct database queries")
        
        cyber_orders = CyberServiceOrder.query.all()
        print(f"Cyber Service Orders: {len(cyber_orders)}")
        
        ecommerce_orders = Order.query.all()
        print(f"Ecommerce Orders: {len(ecommerce_orders)}")
        
        # Test 2: Check if we can access service relationship
        print("\n🔍 Test 2: Service relationship test")
        if cyber_orders:
            order = cyber_orders[0]
            print(f"First order: {order.order_number}")
            print(f"Service: {order.service}")
            if order.service:
                print(f"Service name: {order.service.name}")
                print(f"Service to_dict: {order.service.to_dict()}")
            else:
                print("❌ Service relationship is None!")
        
        # Test 3: Test the to_dict method
        print("\n🔍 Test 3: to_dict method test")
        if cyber_orders:
            order = cyber_orders[0]
            try:
                order_dict = order.to_dict()
                print(f"Order to_dict successful: {len(order_dict)} fields")
                print(f"Keys: {list(order_dict.keys())}")
                if 'service' in order_dict:
                    print(f"Service in dict: {order_dict['service'] is not None}")
            except Exception as e:
                print(f"❌ Error in to_dict: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # Test 4: Check admin users
        print("\n🔍 Test 4: Admin users check")
        admin_users = AdminUser.query.all()
        print(f"Admin users: {len(admin_users)}")
        for admin in admin_users:
            print(f"  - {admin.username} (active: {admin.is_active})")

if __name__ == "__main__":
    test_admin_route() 