#!/usr/bin/env python3
"""
Test script to verify admin access to commissions endpoint
"""
import requests
import json

def test_admin_access():
    base_url = "http://localhost:5000"
    
    print("=" * 60)
    print("🔍 Testing Admin Access to Commissions Endpoint")
    print("=" * 60)
    
    # Test 1: Check if endpoint exists without auth
    print("\n1️⃣ Testing endpoint without authentication...")
    try:
        response = requests.get(f"{base_url}/admin/commissions/users-with-wallets")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Endpoint exists and requires authentication")
        elif response.status_code == 200:
            print("   ⚠️  Endpoint exists but doesn't require authentication")
            try:
                data = response.json()
                print(f"   📊 Data: {json.dumps(data, indent=2)[:300]}...")
            except:
                print("   📄 Response is not JSON")
        else:
            print(f"   ❓ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Check if admin login endpoint exists
    print("\n2️⃣ Testing admin login endpoint...")
    try:
        response = requests.post(f"{base_url}/admin/login", json={
            "email": "admin@kibtech.co.ke",
            "password": "test123"
        })
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Admin login endpoint working")
            try:
                data = response.json()
                if 'token' in data:
                    print("   🔑 Token received")
                    token = data['token']
                    
                    # Test 3: Test with actual token
                    print("\n3️⃣ Testing commissions endpoint with admin token...")
                    headers = {'Authorization': f'Bearer {token}'}
                    response = requests.get(f"{base_url}/admin/commissions/users-with-wallets", headers=headers)
                    print(f"   Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print("   ✅ Successfully accessed with admin token")
                        try:
                            data = response.json()
                            if data.get('status') == 'success':
                                users = data.get('users', [])
                                total_commission = sum(user['wallet']['commission_balance'] for user in users)
                                total_wallet = sum(user['wallet']['balance'] for user in users)
                                print(f"   📊 Total Commission: KSh {total_commission:,.2f}")
                                print(f"   📊 Total Wallet: KSh {total_wallet:,.2f}")
                                print(f"   📊 Total Users: {len(users)}")
                            else:
                                print(f"   ❌ API returned error: {data}")
                        except Exception as e:
                            print(f"   ❌ Error parsing response: {str(e)}")
                    else:
                        print(f"   ❌ Failed to access with token: {response.status_code}")
                        print(f"   Response: {response.text[:200]}...")
                        
                else:
                    print("   ❌ No token in response")
            except Exception as e:
                print(f"   ❌ Error parsing login response: {str(e)}")
        else:
            print(f"   ❌ Admin login failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("   If you see 'Successfully accessed with admin token' above,")
    print("   the backend is working and the issue is in the frontend.")
    print("   If you see authentication errors, the admin needs to login first.")
    print("=" * 60)

if __name__ == "__main__":
    test_admin_access() 