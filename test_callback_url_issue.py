#!/usr/bin/env python3
"""
Test Callback URL Configuration
===============================

This script identifies why M-Pesa callbacks are not being received.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import requests

def test_callback_url_accessibility():
    """Test if the callback URL is accessible from the internet"""
    print("🔍 Testing Callback URL Accessibility")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Get the configured callback URL
            callback_url = app.config.get('MPESA_CALLBACK_URL')
            print(f"1. 🔧 Current Callback URL: {callback_url}")
            
            # Check if it's localhost
            if 'localhost' in callback_url or '127.0.0.1' in callback_url:
                print("   ❌ PROBLEM FOUND: Using localhost URL!")
                print("   🚨 M-Pesa cannot reach localhost from the internet")
                print("   💡 Solution: Use a public URL or ngrok tunnel")
                
                return False
            elif 'kibtech.co.ke' in callback_url:
                print("   ✅ Using production domain")
                
                # Test if the production endpoint is accessible
                try:
                    response = requests.get(f"{callback_url.replace('/callback', '/test-callback')}", timeout=10)
                    if response.status_code == 200:
                        print("   ✅ Production endpoint is accessible")
                        return True
                    else:
                        print(f"   ⚠️ Production endpoint returned: {response.status_code}")
                        return False
                except Exception as e:
                    print(f"   ❌ Cannot reach production endpoint: {str(e)}")
                    return False
            else:
                print("   ℹ️ Using custom domain")
                return True
                
    except Exception as e:
        print(f"❌ Error testing callback URL: {str(e)}")
        return False

def test_local_callback_endpoint():
    """Test if the local callback endpoint is working"""
    print("\n2. 🔧 Testing Local Callback Endpoint")
    print("=" * 50)
    
    try:
        # Test local endpoint
        local_url = "http://localhost:5000/api/mpesa/test-callback"
        
        response = requests.get(local_url, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Local endpoint is working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"   ❌ Local endpoint error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Local endpoint not accessible - Flask not running")
        return False
    except Exception as e:
        print(f"   ❌ Error testing local endpoint: {str(e)}")
        return False

def provide_solutions():
    """Provide solutions for the callback URL issue"""
    print("\n3. 💡 Solutions to Fix Callback URL")
    print("=" * 50)
    
    print("🚨 The Problem:")
    print("   M-Pesa cannot reach http://localhost:5000 from the internet")
    print("   It needs a public URL to send payment confirmations")
    
    print("\n🔧 Quick Fix Options:")
    print("   Option 1: Use ngrok (Recommended for testing)")
    print("      npm install -g ngrok")
    print("      ngrok http 5000")
    print("      Then use the ngrok URL as your callback")
    
    print("\n   Option 2: Use your production domain")
    print("      Set MPESA_CALLBACK_URL=https://kibtech.co.ke/api/mpesa/callback")
    
    print("\n   Option 3: Use localtunnel")
    print("      npm install -g localtunnel")
    print("      lt --port 5000")
    
    print("\n🎯 Recommended Action:")
    print("   1. Install ngrok: npm install -g ngrok")
    print("   2. Run: ngrok http 5000")
    print("   3. Copy the ngrok URL (e.g., https://abc123.ngrok.io)")
    print("   4. Set: MPESA_CALLBACK_URL=https://abc123.ngrok.io/api/mpesa/callback")
    print("   5. Restart Flask and test payment again")

if __name__ == "__main__":
    print("🚀 Callback URL Configuration Test")
    print("=" * 50)
    
    # Test callback URL configuration
    url_ok = test_callback_url_accessibility()
    
    # Test local endpoint
    local_ok = test_local_callback_endpoint()
    
    if not url_ok:
        print("\n❌ Callback URL configuration issue detected!")
        provide_solutions()
    elif not local_ok:
        print("\n❌ Local endpoint issue detected!")
        print("   Please ensure Flask is running on port 5000")
    else:
        print("\n✅ All tests passed!")
        print("   If callbacks still aren't working, check M-Pesa logs") 