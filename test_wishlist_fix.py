#!/usr/bin/env python3
"""
Test script to verify wishlist functionality
"""

import requests
import json
from datetime import datetime

def test_wishlist_api():
    """Test the wishlist API endpoints"""
    
    # Base URL
    base_url = "http://localhost:5000"
    
    # Test user credentials (you may need to adjust these)
    login_data = {
        "email": "test@example.com",  # Replace with actual test user
        "password": "password123"      # Replace with actual password
    }
    
    print("🔧 Testing Wishlist API...")
    print("=" * 50)
    
    try:
        # 1. Login to get token
        print("1. Logging in...")
        login_response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token = login_response.json().get('token')
        if not token:
            print("❌ No token received")
            return
        
        print("✅ Login successful")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Get wishlist count
        print("\n2. Testing wishlist count...")
        count_response = requests.get(f"{base_url}/api/wishlist/count", headers=headers)
        
        if count_response.status_code == 200:
            count_data = count_response.json()
            print(f"✅ Wishlist count: {count_data.get('count', 0)}")
        else:
            print(f"❌ Count request failed: {count_response.status_code}")
            print(f"Response: {count_response.text}")
        
        # 3. Get wishlist items
        print("\n3. Testing wishlist items...")
        items_response = requests.get(f"{base_url}/api/wishlist/", headers=headers)
        
        if items_response.status_code == 200:
            items_data = items_response.json()
            wishlist_items = items_data.get('wishlist_items', [])
            print(f"✅ Wishlist items: {len(wishlist_items)}")
            
            if wishlist_items:
                print("Items found:")
                for item in wishlist_items:
                    product = item.get('product', {})
                    print(f"  - {product.get('name', 'Unknown')} (ID: {product.get('id', 'N/A')})")
            else:
                print("  No items in wishlist")
        else:
            print(f"❌ Items request failed: {items_response.status_code}")
            print(f"Response: {items_response.text}")
        
        # 4. Test adding a product to wishlist (if we have products)
        print("\n4. Testing add to wishlist...")
        
        # First, get some products
        products_response = requests.get(f"{base_url}/api/products/")
        if products_response.status_code == 200:
            products_data = products_response.json()
            products = products_data.get('products', [])
            
            if products:
                test_product = products[0]
                print(f"Testing with product: {test_product.get('name')} (ID: {test_product.get('id')})")
                
                add_data = {"product_id": test_product.get('id')}
                add_response = requests.post(f"{base_url}/api/wishlist/add", 
                                           json=add_data, headers=headers)
                
                if add_response.status_code == 200:
                    print("✅ Product added to wishlist successfully")
                    
                    # Check updated count
                    updated_count_response = requests.get(f"{base_url}/api/wishlist/count", headers=headers)
                    if updated_count_response.status_code == 200:
                        updated_count = updated_count_response.json().get('count', 0)
                        print(f"✅ Updated wishlist count: {updated_count}")
                    
                    # Check updated items
                    updated_items_response = requests.get(f"{base_url}/api/wishlist/", headers=headers)
                    if updated_items_response.status_code == 200:
                        updated_items_data = updated_items_response.json()
                        updated_items = updated_items_data.get('wishlist_items', [])
                        print(f"✅ Updated wishlist items: {len(updated_items)}")
                    
                    # Test removing the product
                    print("\n5. Testing remove from wishlist...")
                    remove_response = requests.delete(f"{base_url}/api/wishlist/remove/{test_product.get('id')}", 
                                                    headers=headers)
                    
                    if remove_response.status_code == 200:
                        print("✅ Product removed from wishlist successfully")
                        
                        # Check final count
                        final_count_response = requests.get(f"{base_url}/api/wishlist/count", headers=headers)
                        if final_count_response.status_code == 200:
                            final_count = final_count_response.json().get('count', 0)
                            print(f"✅ Final wishlist count: {final_count}")
                    else:
                        print(f"❌ Remove failed: {remove_response.status_code}")
                        print(f"Response: {remove_response.text}")
                        
                elif add_response.status_code == 400:
                    error_msg = add_response.json().get('error', 'Unknown error')
                    if 'already in wishlist' in error_msg:
                        print("ℹ️ Product already in wishlist (this is expected if already added)")
                    else:
                        print(f"❌ Add failed: {error_msg}")
                else:
                    print(f"❌ Add failed: {add_response.status_code}")
                    print(f"Response: {add_response.text}")
            else:
                print("ℹ️ No products available to test with")
        else:
            print(f"❌ Failed to get products: {products_response.status_code}")
        
        print("\n" + "=" * 50)
        print("✅ Wishlist API test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_wishlist_api() 