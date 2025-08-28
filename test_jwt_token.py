#!/usr/bin/env python3
"""
Test JWT Token Validation
This script tests JWT token validation to debug the authentication issue.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser
from flask_jwt_extended import create_access_token, decode_token
import requests
import json

def test_jwt_token():
    """Test JWT token validation"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🧪 Testing JWT Token Validation...")
            
            # Get admin user
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            if not admin_user:
                print("❌ Admin user not found!")
                return
            
            print(f"👤 Admin user: {admin_user.email}")
            print(f"🔑 User ID: {admin_user.id}")
            print(f"🔑 Is active: {admin_user.is_active}")
            
            # Create JWT token
            token = create_access_token(identity=str(admin_user.id))
            print(f"🎫 Token created: {token[:50]}...")
            
            # Decode token to verify
            decoded = decode_token(token)
            print(f"🔍 Decoded token identity: {decoded['sub']}")
            
            # Test with profile endpoint
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            print("\n🌐 Testing with profile endpoint...")
            response = requests.get('http://localhost:5000/admin/profile', headers=headers)
            print(f"📊 Profile response status: {response.status_code}")
            print(f"📊 Profile response: {response.text[:200]}...")
            
            # Test with manual commissions endpoint
            print("\n🌐 Testing with manual commissions endpoint...")
            response = requests.get('http://localhost:5000/admin/commissions/manual', headers=headers)
            print(f"📊 Manual commissions response status: {response.status_code}")
            print(f"📊 Manual commissions response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ Manual commissions endpoint working!")
            else:
                print("❌ Manual commissions endpoint failed!")
                print(f"Error details: {response.text}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_jwt_token() 