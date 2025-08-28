#!/usr/bin/env python3
"""
Verify Environment Setup
This script verifies that the .env file is correctly set up and all environment variables are loaded
"""

import os
from dotenv import load_dotenv

def verify_env_file():
    """Verify the .env file has all required variables"""
    
    print("🔍 Verifying .env File")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return False
    
    # Read .env file content
    try:
        with open('.env', 'r') as file:
            content = file.read()
        
        print("✅ .env file found and readable")
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    # Check for required variables
    required_vars = [
        'MPESA_CONSUMER_KEY=',
        'MPESA_CONSUMER_SECRET=',
        'MPESA_SHORTCODE=',
        'MPESA_PASSKEY=',
        'MPESA_INITIATOR_NAME=',
        'MPESA_INITIATOR_PASSWORD=',
        'MPESA_SECURITY_CREDENTIAL=',
        'MPESA_BASE_URL=',
        'MPESA_CALLBACK_URL=',
        'MPESA_RESULT_URL=',
        'MPESA_TIMEOUT_URL='
    ]
    
    print("\n📋 Required Variables Check:")
    print("-" * 40)
    
    missing_vars = []
    for var in required_vars:
        if var in content:
            # Get the value length for display
            lines = content.split('\n')
            for line in lines:
                if line.startswith(var):
                    value = line.replace(var, '').strip()
                    if value:
                        print(f"✅ {var.replace('=', '')}: Set ({len(value)} chars)")
                    else:
                        print(f"❌ {var.replace('=', '')}: Empty")
                        missing_vars.append(var.replace('=', ''))
                    break
        else:
            print(f"❌ {var.replace('=', '')}: Missing")
            missing_vars.append(var.replace('=', ''))
    
    if missing_vars:
        print(f"\n❌ Missing variables: {', '.join(missing_vars)}")
        return False
    else:
        print(f"\n✅ All required variables are present in .env file")
        return True

def verify_environment_loading():
    """Verify that environment variables are properly loaded"""
    
    print(f"\n🔍 Verifying Environment Variable Loading")
    print("=" * 50)
    
    # Load .env file
    load_dotenv()
    
    # Check if variables are accessible via os.environ
    required_vars = [
        'MPESA_CONSUMER_KEY',
        'MPESA_CONSUMER_SECRET',
        'MPESA_SHORTCODE',
        'MPESA_PASSKEY',
        'MPESA_INITIATOR_NAME',
        'MPESA_INITIATOR_PASSWORD',
        'MPESA_SECURITY_CREDENTIAL',
        'MPESA_BASE_URL',
        'MPESA_CALLBACK_URL',
        'MPESA_RESULT_URL',
        'MPESA_TIMEOUT_URL'
    ]
    
    print("📋 Environment Variables Loading Check:")
    print("-" * 40)
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: Loaded ({len(value)} chars)")
        else:
            print(f"❌ {var}: Not loaded")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Variables not loaded: {', '.join(missing_vars)}")
        return False
    else:
        print(f"\n✅ All environment variables are properly loaded")
        return True

def verify_config_loading():
    """Verify that config.py can load the variables"""
    
    print(f"\n🔍 Verifying Config.py Loading")
    print("=" * 50)
    
    try:
        # Import config
        import sys
        sys.path.append('.')
        from config import Config
        
        # Create config instance
        config = Config()
        
        print("📋 Config.py Variables Check:")
        print("-" * 40)
        
        required_vars = [
            'MPESA_CONSUMER_KEY',
            'MPESA_CONSUMER_SECRET',
            'MPESA_SHORTCODE',
            'MPESA_PASSKEY',
            'MPESA_INITIATOR_NAME',
            'MPESA_INITIATOR_PASSWORD',
            'MPESA_SECURITY_CREDENTIAL',
            'MPESA_BASE_URL',
            'MPESA_CALLBACK_URL',
            'MPESA_RESULT_URL',
            'MPESA_TIMEOUT_URL'
        ]
        
        missing_vars = []
        for var in required_vars:
            value = getattr(config, var, None)
            if value:
                print(f"✅ {var}: Loaded ({len(str(value))} chars)")
            else:
                print(f"❌ {var}: Not loaded")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"\n❌ Config variables not loaded: {', '.join(missing_vars)}")
            return False
        else:
            print(f"\n✅ All config variables are properly loaded")
            return True
            
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False

def show_security_credential_details():
    """Show details about the security credential"""
    
    print(f"\n🔐 Security Credential Details")
    print("=" * 50)
    
    # Load .env file
    load_dotenv()
    
    security_credential = os.environ.get('MPESA_SECURITY_CREDENTIAL')
    if security_credential:
        print(f"✅ Security Credential: Present")
        print(f"   Length: {len(security_credential)} characters")
        print(f"   Starts with: {security_credential[:20]}...")
        print(f"   Ends with: ...{security_credential[-20:]}")
        
        # Check if it matches the working one
        working_credential = "PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA=="
        
        if security_credential == working_credential:
            print(f"✅ Matches working B2C credential")
        else:
            print(f"❌ Does NOT match working B2C credential")
            print(f"   This might cause B2C payments to fail")
    else:
        print(f"❌ Security Credential: Not found")

def main():
    """Main function"""
    print("🔍 Environment Setup Verification")
    print("=" * 60)
    
    # Step 1: Verify .env file
    env_file_ok = verify_env_file()
    
    # Step 2: Verify environment loading
    env_loading_ok = verify_environment_loading()
    
    # Step 3: Verify config loading
    config_loading_ok = verify_config_loading()
    
    # Step 4: Show security credential details
    show_security_credential_details()
    
    # Overall status
    print(f"\n🎯 Overall Status:")
    print("=" * 30)
    print(f"📁 .env file: {'✅ OK' if env_file_ok else '❌ FAILED'}")
    print(f"🔄 Environment loading: {'✅ OK' if env_loading_ok else '❌ FAILED'}")
    print(f"⚙️ Config loading: {'✅ OK' if config_loading_ok else '❌ FAILED'}")
    
    if env_file_ok and env_loading_ok and config_loading_ok:
        print(f"\n🎉 All checks passed! Your B2C system should work correctly!")
        print(f"✅ You can now test: python test_b2c_with_actual_config.py")
        return True
    else:
        print(f"\n❌ Some checks failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🎯 Final Status: {'✅ READY' if success else '❌ NEEDS FIXING'}") 