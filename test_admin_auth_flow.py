#!/usr/bin/env python3
"""
Test Admin Authentication Flow
This script tests the admin authentication flow to ensure tokens are working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser
from flask_jwt_extended import create_access_token

def test_admin_auth_flow():
    """Test the admin authentication flow"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🧪 Testing Admin Authentication Flow...")
            
            # Get admin user
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            if not admin_user:
                print("❌ Admin user not found!")
                return
            
            print(f"👤 Admin user: {admin_user.email}")
            print(f"🔑 Is active: {admin_user.is_active}")
            print(f"🔑 Is super admin: {admin_user.is_super_admin}")
            
            # Test JWT token creation
            print(f"\n🎫 Testing JWT token creation...")
            token = create_access_token(identity=str(admin_user.id))
            print(f"✅ Token created: {token[:50]}...")
            
            # Test the token with the profile endpoint
            print(f"\n🌐 Testing token with profile endpoint...")
            
            client = app.test_client()
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get('/admin/profile', headers=headers)
            
            print(f"📊 Profile response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Profile endpoint working!")
                print(f"👤 Admin data: {data.get('data', {}).get('admin', {}).get('email')}")
                print(f"🔑 Permissions: {data.get('data', {}).get('permissions', [])}")
            else:
                print(f"❌ Profile endpoint failed: {response.status_code}")
                print(f"Response: {response.get_json()}")
            
            # Test the manual commissions endpoint with the token
            print(f"\n🌐 Testing manual commissions endpoint...")
            response = client.get('/admin/commissions/manual', headers=headers)
            
            print(f"📊 Manual commissions response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Manual commissions endpoint working!")
                print(f"📋 Commissions returned: {len(data.get('commissions', []))}")
            else:
                print(f"❌ Manual commissions endpoint failed: {response.status_code}")
                print(f"Response: {response.get_json()}")
            
            print(f"\n🎉 Admin authentication flow test completed!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_admin_auth_flow() 