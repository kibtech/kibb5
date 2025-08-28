#!/usr/bin/env python3
"""
Test API Direct Response
Direct test of the API endpoint
"""

import requests
import json

def test_api_direct():
    """Test the API endpoint directly"""
    try:
        print("🔧 Testing API Direct Response...")
        print("=" * 50)
        
        # Test the API endpoint
        url = "http://localhost:5000/api/admin/cyber-services"
        
        # You'll need to get a valid token first
        print("⚠️  Note: This test requires a valid admin token")
        print("Please run this after logging into the admin portal")
        
        # For now, let's just test the endpoint structure
        print(f"\n1. Testing endpoint: {url}")
        
        # Try without token first to see the response
        try:
            response = requests.get(url)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code == 401:
                print("✅ Expected 401 - Authentication required")
            else:
                print(f"Unexpected status: {response.status_code}")
                print(f"Response body: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - Make sure the Flask app is running")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)
        print("✅ API Direct Test Completed!")
        print("\n📝 Next Steps:")
        print("1. Start the Flask app with START_KIBTECH.bat")
        print("2. Login to admin portal")
        print("3. Check browser console for API response logs")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_api_direct() 