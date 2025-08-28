#!/usr/bin/env python3
"""
Test script to verify admin endpoints are working correctly
"""

import requests
import json

def test_admin_endpoint():
    """Test the admin users-with-wallets endpoint"""
    
    # Base URL
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("🔍 Testing Admin Endpoint: /admin/commissions/users-with-wallets")
    print("=" * 60)
    
    # First, try to get the endpoint without authentication
    print("\n1️⃣ Testing endpoint without authentication...")
    try:
        response = requests.get(f"{base_url}/admin/commissions/users-with-wallets")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test with a dummy token
    print("\n2️⃣ Testing endpoint with dummy token...")
    try:
        headers = {'Authorization': 'Bearer dummy_token'}
        response = requests.get(f"{base_url}/admin/commissions/users-with-wallets", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test the endpoint structure
    print("\n3️⃣ Testing endpoint structure...")
    try:
        response = requests.get(f"{base_url}/admin/commissions/users-with-wallets")
        if response.status_code == 401:
            print("   ✅ Endpoint exists and requires authentication (401 Unauthorized)")
        elif response.status_code == 200:
            print("   ⚠️  Endpoint exists but doesn't require authentication (200 OK)")
            try:
                data = response.json()
                print(f"   📊 Data structure: {json.dumps(data, indent=2)[:300]}...")
            except:
                print("   📄 Response is not JSON")
        else:
            print(f"   ❓ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("   1. Check if Flask server is running")
    print("   2. Verify admin authentication is working")
    print("   3. Check browser console for errors")
    print("   4. Verify the endpoint URL in browser network tab")
    print("=" * 60)

if __name__ == "__main__":
    test_admin_endpoint() 