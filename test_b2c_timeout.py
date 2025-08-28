#!/usr/bin/env python3
"""
Test B2C API timeout and configuration
"""

import os
import sys
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Withdrawal
from app.mpesa.services import MpesaService

def test_b2c_timeout():
    """Test B2C payment with timeout handling"""
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing B2C Payment Timeout...")
        
        # Find a test user
        user = User.query.filter_by(email='kashdyke@gmail.com').first()
        if not user:
            print("❌ Test user not found")
            return
        
        print(f"👤 Test user: {user.name} ({user.email})")
        
        # Check M-Pesa configuration
        print("\n📋 M-Pesa Configuration:")
        print(f"  Base URL: {app.config.get('MPESA_BASE_URL', 'Not set')}")
        print(f"  Consumer Key: {app.config.get('MPESA_CONSUMER_KEY', 'Not set')[:10]}..." if app.config.get('MPESA_CONSUMER_KEY') else "  Consumer Key: Not set")
        print(f"  Shortcode: {app.config.get('MPESA_SHORTCODE', 'Not set')}")
        print(f"  Initiator Name: {app.config.get('MPESA_INITIATOR_NAME', 'Not set')}")
        print(f"  Environment: {app.config.get('ENVIRONMENT', 'Not set')}")
        
        # Test access token
        print("\n🔑 Testing Access Token...")
        try:
            mpesa_service = MpesaService()
            start_time = time.time()
            token = mpesa_service.get_access_token()
            end_time = time.time()
            
            print(f"✅ Access token obtained in {end_time - start_time:.2f} seconds")
            print(f"   Token: {token[:20]}..." if token else "   Token: None")
            
        except Exception as e:
            print(f"❌ Access token failed: {str(e)}")
            return
        
        # Test B2C payment with timeout
        print("\n💳 Testing B2C Payment...")
        try:
            start_time = time.time()
            
            # Test with a small amount and test phone number
            response = mpesa_service.b2c_payment(
                phone_number="254712591937",  # Test phone number
                amount=1,  # 1 KSh test amount
                remarks="Test withdrawal"
            )
            
            end_time = time.time()
            
            print(f"⏱️  B2C request completed in {end_time - start_time:.2f} seconds")
            print(f"📊 Response: {response}")
            
            if 'ConversationID' in response:
                print("✅ B2C initiated successfully")
            elif 'error' in response:
                print(f"❌ B2C failed: {response['error']}")
            else:
                print(f"⚠️  Unexpected response: {response}")
                
        except Exception as e:
            print(f"❌ B2C test failed: {str(e)}")
        
        print("\n🎉 B2C timeout test completed!")

if __name__ == "__main__":
    test_b2c_timeout() 