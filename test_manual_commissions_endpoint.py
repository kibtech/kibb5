#!/usr/bin/env python3
"""
Test Manual Commissions Endpoint
This script tests the manual commissions endpoint to ensure it's working correctly.
"""

import sys
import os
import requests
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser, User, Commission

def test_manual_commissions_endpoint():
    """Test the manual commissions endpoint"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🧪 Testing Manual Commissions Endpoint...")
            
            # Get admin user
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            if not admin_user:
                print("❌ Admin user not found!")
                return
            
            print(f"👤 Admin user: {admin_user.email}")
            print(f"🔑 Permissions: {admin_user.role.permissions if admin_user.role else 'No role'}")
            
            # Test permission check
            has_view = admin_user.has_permission('view_commissions')
            has_manage = admin_user.has_permission('manage_commissions')
            print(f"🧪 Permission test: view_commissions={has_view}, manage_commissions={has_manage}")
            
            # Check if there are any users with wallets
            users_with_wallets = User.query.filter(User.wallet.isnot(None)).limit(5).all()
            print(f"👥 Users with wallets: {len(users_with_wallets)}")
            
            # Check existing manual commissions
            manual_commissions = Commission.query.filter(
                Commission.commission_type.in_(['manual', 'manual_removal'])
            ).all()
            print(f"💰 Existing manual commissions: {len(manual_commissions)}")
            
            # Test the endpoint directly
            print(f"\n🌐 Testing endpoint: GET /admin/commissions/manual")
            
            # Create a test client
            client = app.test_client()
            
            # First, we need to get a JWT token by logging in
            login_response = client.post('/admin/login', 
                json={'email': 'kibtechc@gmail.com', 'password': 'admin123'})
            
            if login_response.status_code != 200:
                print(f"❌ Login failed: {login_response.status_code}")
                print(f"Response: {login_response.get_json()}")
                return
            
            login_data = login_response.get_json()
            token = login_data['data']['token']
            print(f"✅ Login successful, got token: {token[:20]}...")
            
            # Test the manual commissions endpoint
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get('/admin/commissions/manual', headers=headers)
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Endpoint working correctly!")
                print(f"📋 Commissions returned: {len(data.get('commissions', []))}")
                print(f"📄 Pagination info: {data.get('pagination', {})}")
            else:
                print(f"❌ Endpoint failed: {response.status_code}")
                print(f"Response: {response.get_json()}")
            
            print(f"\n🎉 Manual commissions endpoint test completed!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_manual_commissions_endpoint() 