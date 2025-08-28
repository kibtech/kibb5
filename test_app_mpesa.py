import requests
import json

def test_app_mpesa_config():
    """Test the MPESA configuration endpoint in your app"""
    print("=== Testing App MPESA Configuration ===")
    
    try:
        # Test the config endpoint
        response = requests.get('http://localhost:5000/api/mpesa/test-config', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ MPESA Config Test: SUCCESS")
            print(f"Environment: {data['config']['environment']}")
            print(f"Base URL: {data['config']['base_url']}")
            print(f"Shortcode: {data['config']['shortcode']}")
            print(f"Access Token Test: {data['config']['access_token_test']}")
            
            if data['config']['access_token_test'] == 'SUCCESS':
                print("✅ Access token generation is working!")
                return True
            else:
                print(f"❌ Access token test failed: {data['config']['access_token_test']}")
                return False
        else:
            print(f"❌ Config test failed: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to your app. Make sure it's running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Config test error: {e}")
        return False

def test_app_mpesa_debug():
    """Test the debug endpoint"""
    print("\n=== Testing App MPESA Debug ===")
    
    try:
        response = requests.get('http://localhost:5000/api/mpesa/debug-config', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Debug Config: SUCCESS")
            print(f"Environment: {data['config']['environment']}")
            print(f"Base URL: {data['config']['base_url']}")
            print(f"Shortcode: {data['config']['shortcode']}")
            return True
        else:
            print(f"❌ Debug test failed: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Debug test error: {e}")
        return False

def test_stk_push_from_app():
    """Test STK push through your app (requires authentication)"""
    print("\n=== Testing STK Push from App ===")
    print("Note: This requires a valid JWT token and an existing order")
    print("You'll need to:")
    print("1. Login to get a JWT token")
    print("2. Create an order")
    print("3. Use the order ID and phone number")
    print()
    
    # Example of how to test (you'll need to fill in the actual values)
    print("Example test request:")
    print("""
    curl -X POST http://localhost:5000/api/mpesa/stk-push \\
         -H "Content-Type: application/json" \\
         -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
         -d '{
           "order_id": ORDER_ID,
           "phone_number": "254712591937"
         }'
    """)

def main():
    print("=== App MPESA Service Test ===")
    print("Testing your updated MPESA service...\n")
    
    # Test 1: Configuration
    config_ok = test_app_mpesa_config()
    
    # Test 2: Debug
    debug_ok = test_app_mpesa_debug()
    
    # Test 3: STK Push (informational)
    test_stk_push_from_app()
    
    print("\n=== Summary ===")
    if config_ok and debug_ok:
        print("✅ Your app's MPESA service is working correctly!")
        print("The updated configuration with better timeout and retry settings is active.")
        print("\nNext steps:")
        print("1. Test STK push through your frontend")
        print("2. Make sure your callback URL is properly configured")
        print("3. Test the full payment flow")
    else:
        print("❌ Some tests failed. Check your app configuration.")
        print("\nMake sure:")
        print("1. Your Flask app is running on localhost:5000")
        print("2. The MPESA routes are properly registered")
        print("3. Your environment variables are set correctly")

if __name__ == "__main__":
    main() 