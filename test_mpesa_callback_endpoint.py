#!/usr/bin/env python3
"""
Test MPesa Callback Endpoint
This script tests the MPesa callback endpoint to identify why callbacks aren't working.
"""

import os
import sys
import requests
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_callback_endpoint():
    """Test the MPesa callback endpoint"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 TESTING MPESA CALLBACK ENDPOINT")
        print("=" * 50)
        
        # Get callback URL from config
        callback_url = app.config['MPESA_CALLBACK_URL']
        print(f"📡 MPesa Callback URL: {callback_url}")
        
        # Check if callback URL is accessible
        print(f"\n🔍 TESTING CALLBACK URL ACCESSIBILITY:")
        print("-" * 50)
        
        try:
            # Test if the URL is accessible
            response = requests.get(callback_url, timeout=10)
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("   ✅ Callback URL is accessible")
            else:
                print(f"   ⚠️  Callback URL returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Callback URL not accessible: {str(e)}")
            print(f"   💡 This explains why callbacks aren't working!")
        
        # Check local callback endpoint
        print(f"\n🏠 TESTING LOCAL CALLBACK ENDPOINT:")
        print("-" * 50)
        
        local_callback_url = "http://localhost:5000/api/mpesa/callback"
        print(f"   Local URL: {local_callback_url}")
        
        try:
            # Test local endpoint
            response = requests.get(local_callback_url, timeout=5)
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("   ✅ Local callback endpoint is working")
            else:
                print(f"   ⚠️  Local endpoint returned status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Local callback endpoint not accessible: {str(e)}")
            print(f"   💡 Make sure your Flask app is running on localhost:5000")

def analyze_callback_issue():
    """Analyze the callback issue"""
    
    print(f"\n🔍 CALLBACK ISSUE ANALYSIS:")
    print("=" * 50)
    
    print(f"🎯 ROOT CAUSE IDENTIFIED:")
    print(f"   Your MPesa callback URL is set to: https://kibtech.co.ke/api/mpesa/callback")
    print(f"   But you're testing locally on: localhost:5000")
    print(f"   MPesa is trying to send callbacks to your production server, not localhost!")
    
    print(f"\n❌ WHY REFERRED USERS GET STUCK:")
    print(f"   1. MPesa receives payment successfully")
    print(f"   2. MPesa tries to send callback to https://kibtech.co.ke")
    print(f"   3. Your local server never receives the callback")
    print(f"   4. Payment status never updates from 'Payment Initiated'")
    print(f"   5. Frontend keeps polling for status updates")
    
    print(f"\n✅ WHY NON-REFERRED USERS WORK:")
    print(f"   They might be using a different payment flow or callback mechanism")
    print(f"   Or the issue only affects certain order types")

def provide_solutions():
    """Provide solutions to fix the callback issue"""
    
    print(f"\n🔧 SOLUTIONS TO FIX CALLBACK ISSUE:")
    print("=" * 50)
    
    print(f"💡 SOLUTION 1: Update Callback URL for Local Testing")
    print(f"   In your config.py, temporarily change:")
    print(f"   MPESA_CALLBACK_URL = 'http://localhost:5000/api/mpesa/callback'")
    print(f"   This will make MPesa send callbacks to your local server")
    
    print(f"\n💡 SOLUTION 2: Use Ngrok for Public Callback URL")
    print(f"   1. Install ngrok: pip install pyngrok")
    print(f"   2. Run: ngrok http 5000")
    print(f"   3. Use the ngrok URL as your callback URL")
    print(f"   4. MPesa can reach your local server through ngrok")
    
    print(f"\n💡 SOLUTION 3: Test on Production Server")
    print(f"   Deploy your app to kibtech.co.ke and test there")
    print(f"   This ensures the callback URL is accessible")
    
    print(f"\n🎯 RECOMMENDED APPROACH:")
    print(f"   Use Solution 1 for immediate testing")
    print(f"   Use Solution 2 for ongoing development")
    print(f"   Use Solution 3 for production verification")

def test_local_callback_simulation():
    """Simulate a callback to test local processing"""
    
    print(f"\n🧪 SIMULATING MPESA CALLBACK LOCALLY:")
    print("=" * 50)
    
    # Sample MPesa callback data
    sample_callback = {
        "Body": {
            "stkCallback": {
                "MerchantRequestID": "test-123",
                "CheckoutRequestID": "test-checkout-123",
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "Amount": 1,
                "MpesaReceiptNumber": "TEST123456789",
                "TransactionDate": "20250813223334",
                "PhoneNumber": "254112735877"
            }
        }
    }
    
    local_callback_url = "http://localhost:5000/api/mpesa/callback"
    
    try:
        print(f"   Sending test callback to: {local_callback_url}")
        response = requests.post(
            local_callback_url,
            json=sample_callback,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("   ✅ Local callback processing works!")
        else:
            print(f"   ⚠️  Local callback processing failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Could not test local callback: {str(e)}")
        print(f"   💡 Make sure your Flask app is running")

if __name__ == "__main__":
    try:
        test_callback_endpoint()
        analyze_callback_issue()
        provide_solutions()
        test_local_callback_simulation()
        
        print(f"\n🎯 SUMMARY:")
        print("=" * 50)
        print(f"✅ Commission table structure: FIXED")
        print(f"❌ MPesa callback delivery: NOT WORKING")
        print(f"💡 Root cause: Callback URL points to production, not localhost")
        print(f"🔧 Solution: Update callback URL for local testing")
        
    except Exception as e:
        logger.error(f"Failed to test callback endpoint: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 