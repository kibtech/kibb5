#!/usr/bin/env python3
"""
Test all endpoints with the same JWT token to identify the issue
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, db
from flask_jwt_extended import create_access_token

def test_all_endpoints():
    """Test all endpoints with the same JWT token"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing All Endpoints with Same JWT Token...")
        print("=" * 60)
        
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
        
        # Test all endpoints
        endpoints_to_test = [
            '/api/auth/referral-stats',
            '/api/wallet/stats', 
            '/api/cart/count',
            '/api/wishlist/count',
            '/api/notifications/',
            '/api/auth/profile'
        ]
        
        with app.test_client() as client:
            headers = {'Authorization': f'Bearer {token}'}
            
            for endpoint in endpoints_to_test:
                print(f"\n🔍 Testing {endpoint}...")
                try:
                    response = client.get(endpoint, headers=headers)
                    status = response.status_code
                    
                    if status == 200:
                        print(f"   ✅ {endpoint}: {status}")
                        if 'referral-stats' in endpoint:
                            data = response.get_json()
                            print(f"      Referral Code: {data.get('referral_code')}")
                            print(f"      Total Referrals: {data.get('total_referrals')}")
                    elif status == 403:
                        print(f"   ❌ {endpoint}: {status} (FORBIDDEN)")
                        print(f"      Response: {response.get_data(as_text=True)}")
                    else:
                        print(f"   ⚠️  {endpoint}: {status}")
                        print(f"      Response: {response.get_data(as_text=True)}")
                        
                except Exception as e:
                    print(f"   💥 {endpoint}: ERROR - {str(e)}")
        
        return True

if __name__ == "__main__":
    print("🚀 All Endpoints Tester")
    print("=" * 60)
    
    try:
        success = test_all_endpoints()
        if success:
            print("\n✅ Test completed!")
        else:
            print("\n❌ Test failed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 