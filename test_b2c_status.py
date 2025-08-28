import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_b2c_config():
    """Check B2C configuration status"""
    print("=== B2C Configuration Status ===")
    print()
    
    # Check environment variables
    config_vars = {
        'MPESA_INITIATOR_NAME': os.environ.get('MPESA_INITIATOR_NAME'),
        'MPESA_INITIATOR_PASSWORD': os.environ.get('MPESA_INITIATOR_PASSWORD'),
        'MPESA_RESULT_URL': os.environ.get('MPESA_RESULT_URL'),
        'MPESA_TIMEOUT_URL': os.environ.get('MPESA_TIMEOUT_URL')
    }
    
    print("Environment Variables:")
    for var, value in config_vars.items():
        if value:
            if 'PASSWORD' in var:
                print(f"✅ {var}: {'*' * len(value)} (configured)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not configured")
    
    print()
    
    # Check if all required variables are set
    required_vars = ['MPESA_INITIATOR_NAME', 'MPESA_INITIATOR_PASSWORD']
    missing_vars = [var for var in required_vars if not config_vars[var]]
    
    if missing_vars:
        print("❌ B2C Configuration: INCOMPLETE")
        print(f"Missing variables: {', '.join(missing_vars)}")
        print()
        print("To fix this:")
        print("1. Add the missing variables to your .env file")
        print("2. Or set them as environment variables")
        print()
        print("Example .env entries:")
        print("MPESA_INITIATOR_NAME=your_initiator_name")
        print("MPESA_INITIATOR_PASSWORD=your_initiator_password")
        print("MPESA_RESULT_URL=https://kibtech.co.ke/api/mpesa/b2c-result")
        print("MPESA_TIMEOUT_URL=https://kibtech.co.ke/api/mpesa/timeout")
        return False
    else:
        print("✅ B2C Configuration: COMPLETE")
        print("All required variables are configured.")
        return True

def check_app_config():
    """Check app configuration"""
    print("\n=== App Configuration Check ===")
    
    try:
        import requests
        response = requests.get('http://localhost:5000/api/mpesa/debug-config', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ App is running and accessible")
            print(f"Environment: {data['config']['environment']}")
            print(f"Base URL: {data['config']['base_url']}")
            print(f"Shortcode: {data['config']['shortcode']}")
            return True
        else:
            print(f"❌ App returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ App is not running on localhost:5000")
        print("Start your Flask app first: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error checking app: {e}")
        return False

def main():
    print("=== B2C Withdrawal Status Check ===")
    print()
    
    # Check configuration
    config_ok = check_b2c_config()
    
    # Check app
    app_ok = check_app_config()
    
    print("\n=== Summary ===")
    if config_ok and app_ok:
        print("✅ B2C is ready for testing!")
        print("\nNext steps:")
        print("1. Run: python test_withdrawal.py")
        print("2. Test withdrawal through your frontend")
    elif config_ok and not app_ok:
        print("⚠️  Configuration is ready, but app is not running")
        print("\nNext steps:")
        print("1. Start your Flask app: python run.py")
        print("2. Then test B2C functionality")
    elif not config_ok and app_ok:
        print("❌ App is running, but B2C configuration is incomplete")
        print("\nNext steps:")
        print("1. Configure B2C credentials in .env file")
        print("2. Restart your app")
        print("3. Then test B2C functionality")
    else:
        print("❌ Both configuration and app need attention")
        print("\nNext steps:")
        print("1. Configure B2C credentials")
        print("2. Start your Flask app")
        print("3. Then test B2C functionality")

if __name__ == "__main__":
    main() 