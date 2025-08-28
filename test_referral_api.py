#!/usr/bin/env python3
"""
Script to test the referral API endpoints directly
"""
import os
import sys
import requests
import json

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, db

def test_referral_api():
    """Test the referral API endpoints"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing Referral API Endpoints...")
        print("=" * 50)
        
        # Get user JOY
        user = db.session.query(User).filter_by(name='JOY').first()
        if not user:
            print("❌ User 'JOY' not found!")
            return False
        
        print(f"✅ Testing for user: {user.name} (ID: {user.id})")
        print(f"   Referral Code: {user.referral_code}")
        
        # Test the referral-stats endpoint using the app's test client
        with app.test_client() as client:
            print("\n🔍 Testing /api/auth/referral-stats endpoint...")
            
            # First login to get JWT token
            login_data = {
                'email': user.email,
                'password': 'password123'  # You might need to adjust this
            }
            
            print(f"   Attempting login with email: {user.email}")
            login_response = client.post('/api/auth/login', 
                                       data=json.dumps(login_data),
                                       content_type='application/json')
            
            print(f"   Login status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                login_result = login_response.get_json()
                token = login_result.get('access_token')
                print(f"   ✅ Login successful, got token")
                
                # Test referral-stats endpoint
                headers = {'Authorization': f'Bearer {token}'}
                referral_response = client.get('/api/auth/referral-stats', headers=headers)
                
                print(f"   Referral stats status: {referral_response.status_code}")
                print(f"   Referral stats response: {referral_response.get_data(as_text=True)}")
                
                if referral_response.status_code == 200:
                    referral_data = referral_response.get_json()
                    print(f"   ✅ Referral code in response: {referral_data.get('referral_code')}")
                    print(f"   ✅ Total referrals: {referral_data.get('total_referrals', 0)}")
                    print(f"   ✅ Total earned: {referral_data.get('total_earned', 0)}")
                else:
                    print(f"   ❌ Referral stats endpoint failed")
                
                # Test wallet stats endpoint
                print(f"\n🔍 Testing /api/wallet/stats endpoint...")
                wallet_response = client.get('/api/wallet/stats', headers=headers)
                
                print(f"   Wallet stats status: {wallet_response.status_code}")
                print(f"   Wallet stats response: {wallet_response.get_data(as_text=True)}")
                
            else:
                print(f"   ❌ Login failed: {login_response.get_data(as_text=True)}")
                
                # Let's try to test without authentication requirements
                print(f"\n🔍 Testing referral stats logic directly...")
                
                # Import the function directly
                from app.auth.routes import referral_stats
                from flask_jwt_extended import create_access_token
                
                # Create a token for the user
                with app.app_context():
                    token = create_access_token(identity=user.id)
                    
                    # Mock the JWT context
                    with app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                        try:
                            # This would require proper JWT setup, let's check the endpoint code instead
                            print(f"   Token created for user {user.id}")
                        except Exception as e:
                            print(f"   Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Referral API Tester")
    print("=" * 50)
    
    try:
        test_referral_api()
        print("\n✅ API test completed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()