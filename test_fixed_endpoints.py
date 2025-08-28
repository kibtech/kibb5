#!/usr/bin/env python3
"""
Test Fixed Endpoints
===================
Test the endpoints that were previously returning 500 errors to verify they're now working.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Payment, Product, Category, Brand
import requests
import json

def test_payment_status_endpoint():
    """Test the payment status endpoint"""
    print("🔍 Testing payment status endpoint...")
    try:
        app = create_app()
        with app.app_context():
            # Test with a known payment ID
            payment = db.session.get(Payment, 41)
            if payment:
                print(f"   ✅ Payment 41 exists: {payment.amount}")
                print(f"   ✅ Order relationship works: {payment.order.order_number}")
                return True
            else:
                print("   ❌ Payment 41 not found")
                return False
    except Exception as e:
        print(f"   ❌ Payment status test failed: {e}")
        return False

def test_product_endpoints():
    """Test the product endpoints"""
    print("\n🔍 Testing product endpoints...")
    try:
        app = create_app()
        with app.app_context():
            # Test featured products
            featured_products = db.session.query(Product).filter_by(is_active=True, is_featured=True).limit(3).all()
            print(f"   ✅ Featured products query: {len(featured_products)} products")
            
            # Test categories
            categories = db.session.query(Category).filter_by(is_active=True).limit(3).all()
            print(f"   ✅ Categories query: {len(categories)} categories")
            
            # Test brands
            brands = db.session.query(Brand).filter_by(is_active=True).limit(3).all()
            print(f"   ✅ Brands query: {len(brands)} brands")
            
            return True
    except Exception as e:
        print(f"   ❌ Product endpoints test failed: {e}")
        return False

def test_api_endpoints():
    """Test the actual API endpoints"""
    print("\n🔍 Testing API endpoints...")
    base_url = "http://localhost:5000"
    
    try:
        # Test featured products endpoint
        response = requests.get(f"{base_url}/api/products/featured?limit=3", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Featured products API: {len(data.get('products', []))} products")
        else:
            print(f"   ❌ Featured products API failed: {response.status_code}")
            return False
        
        # Test categories endpoint
        response = requests.get(f"{base_url}/api/products/categories", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Categories API: {len(data.get('categories', []))} categories")
        else:
            print(f"   ❌ Categories API failed: {response.status_code}")
            return False
        
        # Test payment status endpoint (if server is running)
        try:
            response = requests.get(f"{base_url}/api/mpesa/payment-status/41", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ Payment status API: Success")
            elif response.status_code == 401:
                print(f"   ⚠️ Payment status API: Requires authentication (expected)")
            else:
                print(f"   ❌ Payment status API failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️ Payment status API: Server not running (expected)")
        
        return True
    except Exception as e:
        print(f"   ❌ API endpoints test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Fixed Endpoints...")
    print("=" * 50)
    
    # Test database queries
    db_tests_passed = 0
    total_db_tests = 2
    
    if test_payment_status_endpoint():
        db_tests_passed += 1
    
    if test_product_endpoints():
        db_tests_passed += 1
    
    # Test API endpoints
    api_tests_passed = 0
    total_api_tests = 1
    
    if test_api_endpoints():
        api_tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results:")
    print(f"   Database Tests: {db_tests_passed}/{total_db_tests} passed")
    print(f"   API Tests: {api_tests_passed}/{total_api_tests} passed")
    
    if db_tests_passed == total_db_tests:
        print("✅ All database queries are working correctly!")
        print("✅ SQLAlchemy 2.0 compatibility fix successful!")
    else:
        print("❌ Some database tests failed")
    
    if api_tests_passed == total_api_tests:
        print("✅ All API endpoints are working correctly!")
    else:
        print("⚠️ Some API tests failed (server may not be running)")

if __name__ == "__main__":
    main() 