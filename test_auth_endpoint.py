#!/usr/bin/env python3
"""
Test the auth endpoint directly to see what's causing 403 errors
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, db
from flask_jwt_extended import create_access_token

def test_auth_endpoint():
    """Test the auth endpoint directly"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing Auth Endpoint Directly...")
        print("=" * 50)
        
        # Find user JOY
        user = db.session.query(User).filter_by(name='JOY').first()
        if not user:
            print("❌ User 'JOY' not found!")
            return False
        
        print(f"✅ Found user: {user.name}")
        print(f"   User ID: {user.id}")
        
        # Create a fresh token
        token = create_access_token(identity=str(user.id))
        print(f"   Fresh token created: {token[:50]}...")
        
        # Test the endpoint with the test client
        with app.test_client() as client:
            print(f"\n🔍 Testing /api/auth/referral-stats endpoint...")
            
            headers = {'Authorization': f'Bearer {token}'}
            response = client.get('/api/auth/referral-stats', headers=headers)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.get_data(as_text=True)}")
            
            if response.status_code == 200:
                print(f"   ✅ Endpoint working!")
                data = response.get_json()
                print(f"   Referral Code: {data.get('referral_code')}")
                print(f"   Total Referrals: {data.get('total_referrals')}")
            else:
                print(f"   ❌ Endpoint failed with status {response.status_code}")
        
        return True

if __name__ == "__main__":
    print("🚀 Auth Endpoint Tester")
    print("=" * 50)
    
    try:
        success = test_auth_endpoint()
        if success:
            print("\n✅ Test completed successfully!")
        else:
            print("\n❌ Test failed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 