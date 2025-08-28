#!/usr/bin/env python3
"""
M-Pesa B2C Setup Script
=======================
Configure and test M-Pesa B2C withdrawal functionality.
"""

import os
import sys
from dotenv import load_dotenv

def setup_mpesa_b2c():
    """Setup M-Pesa B2C credentials"""
    
    print("🚀 M-Pesa B2C Setup")
    print("=" * 50)
    
    # Load existing .env file
    load_dotenv()
    
    print("📋 Current M-Pesa Configuration:")
    print(f"   - Consumer Key: {os.getenv('MPESA_CONSUMER_KEY', 'Not set')[:20]}...")
    print(f"   - Consumer Secret: {os.getenv('MPESA_CONSUMER_SECRET', 'Not set')[:20]}...")
    print(f"   - Shortcode: {os.getenv('MPESA_SHORTCODE', 'Not set')}")
    print(f"   - Passkey: {os.getenv('MPESA_PASSKEY', 'Not set')[:20]}...")
    print(f"   - Initiator Name: {os.getenv('MPESA_INITIATOR_NAME', 'Not set')}")
    print(f"   - Initiator Password: {'Set' if os.getenv('MPESA_INITIATOR_PASSWORD') else 'Not set'}")
    print(f"   - Environment: {os.getenv('ENVIRONMENT', 'production')}")
    
    print("\n🔧 B2C Configuration Required:")
    print("   For M-Pesa B2C withdrawals, you need:")
    print("   1. Initiator Name (your business name)")
    print("   2. Initiator Password (encrypted)")
    print("   3. Security Credential (encrypted initiator password)")
    
    print("\n📝 Please provide the following details:")
    
    # Get B2C credentials
    initiator_name = input("   Initiator Name (e.g., 'KibTech Store'): ").strip()
    initiator_password = input("   Initiator Password: ").strip()
    
    if not initiator_name or not initiator_password:
        print("❌ Initiator credentials are required for B2C withdrawals!")
        return
    
    # Update .env file
    env_file = '.env'
    env_content = []
    
    # Read existing .env file
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_content = f.readlines()
    
    # Update or add B2C credentials
    updated = False
    for i, line in enumerate(env_content):
        if line.startswith('MPESA_INITIATOR_NAME='):
            env_content[i] = f'MPESA_INITIATOR_NAME={initiator_name}\n'
            updated = True
            break
        elif line.startswith('MPESA_INITIATOR_PASSWORD='):
            env_content[i] = f'MPESA_INITIATOR_PASSWORD={initiator_password}\n'
            updated = True
            break
    
    # Add if not found
    if not any(line.startswith('MPESA_INITIATOR_NAME=') for line in env_content):
        env_content.append(f'MPESA_INITIATOR_NAME={initiator_name}\n')
    if not any(line.startswith('MPESA_INITIATOR_PASSWORD=') for line in env_content):
        env_content.append(f'MPESA_INITIATOR_PASSWORD={initiator_password}\n')
    
    # Write updated .env file
    with open(env_file, 'w') as f:
        f.writelines(env_content)
    
    print(f"\n✅ B2C credentials updated in {env_file}")
    print(f"   - Initiator Name: {initiator_name}")
    print(f"   - Initiator Password: {'*' * len(initiator_password)}")
    
    print("\n🔗 Callback URLs (make sure these are accessible):")
    print(f"   - Result URL: {os.getenv('MPESA_RESULT_URL', 'http://localhost:5000/api/mpesa/b2c-result')}")
    print(f"   - Timeout URL: {os.getenv('MPESA_TIMEOUT_URL', 'http://localhost:5000/api/mpesa/timeout')}")
    
    print("\n🧪 Next steps:")
    print("   1. Restart your Flask application")
    print("   2. Test the withdrawal functionality")
    print("   3. Check M-Pesa logs for any errors")

def test_mpesa_config():
    """Test M-Pesa configuration"""
    
    print("\n🧪 Testing M-Pesa Configuration")
    print("=" * 50)
    
    load_dotenv()
    
    # Check required fields
    required_fields = [
        'MPESA_CONSUMER_KEY',
        'MPESA_CONSUMER_SECRET', 
        'MPESA_SHORTCODE',
        'MPESA_PASSKEY',
        'MPESA_INITIATOR_NAME',
        'MPESA_INITIATOR_PASSWORD'
    ]
    
    missing_fields = []
    for field in required_fields:
        if not os.getenv(field):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing required fields: {', '.join(missing_fields)}")
        return False
    
    print("✅ All required M-Pesa fields are configured")
    
    # Test access token
    try:
        from app.mpesa.services import MpesaService
        mpesa_service = MpesaService()
        access_token = mpesa_service.get_access_token()
        
        if 'access_token' in access_token:
            print("✅ Access token obtained successfully")
            return True
        else:
            print(f"❌ Failed to get access token: {access_token}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing M-Pesa configuration: {str(e)}")
        return False

if __name__ == "__main__":
    setup_mpesa_b2c()
    test_mpesa_config() 