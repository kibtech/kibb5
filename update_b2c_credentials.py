#!/usr/bin/env python3
"""
Update B2C Credentials
Update M-Pesa B2C credentials with provided initiator details
"""

import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def update_b2c_credentials():
    """Update B2C credentials with provided details"""
    
    print("🔧 Updating B2C Credentials")
    print("=" * 50)
    
    # Provided credentials
    initiator_name = "GEOFFREYKIBET"
    initiator_password = "Kibtechceo@2018"
    
    print(f"📝 Using credentials:")
    print(f"   - Initiator Name: {initiator_name}")
    print(f"   - Password: {initiator_password}")
    
    # Generate security credential (this is what M-Pesa expects)
    try:
        # Create security credential (this is a simplified version)
        # In production, you'd use the actual M-Pesa security credential generation
        security_credential = base64.b64encode(initiator_password.encode()).decode()
        
        print(f"   - Security Credential: {security_credential[:20]}...")
        
    except Exception as e:
        print(f"❌ Error generating security credential: {str(e)}")
        return False
    
    # Update .env file
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"❌ {env_file} file not found!")
        return False
    
    try:
        # Read current .env file
        with open(env_file, 'r') as f:
            env_content = f.readlines()
        
        # Update or add B2C credentials
        updated = False
        
        for i, line in enumerate(env_content):
            if line.startswith('MPESA_INITIATOR_NAME='):
                env_content[i] = f'MPESA_INITIATOR_NAME={initiator_name}\n'
                updated = True
                print("✅ Updated MPESA_INITIATOR_NAME")
            elif line.startswith('MPESA_INITIATOR_PASSWORD='):
                env_content[i] = f'MPESA_INITIATOR_PASSWORD={initiator_password}\n'
                updated = True
                print("✅ Updated MPESA_INITIATOR_PASSWORD")
            elif line.startswith('MPESA_SECURITY_CREDENTIAL='):
                env_content[i] = f'MPESA_SECURITY_CREDENTIAL={security_credential}\n'
                updated = True
                print("✅ Updated MPESA_SECURITY_CREDENTIAL")
        
        # Add missing credentials if not found
        if not any(line.startswith('MPESA_INITIATOR_NAME=') for line in env_content):
            env_content.append(f'MPESA_INITIATOR_NAME={initiator_name}\n')
            print("✅ Added MPESA_INITIATOR_NAME")
        
        if not any(line.startswith('MPESA_INITIATOR_PASSWORD=') for line in env_content):
            env_content.append(f'MPESA_INITIATOR_PASSWORD={initiator_password}\n')
            print("✅ Added MPESA_INITIATOR_PASSWORD")
        
        if not any(line.startswith('MPESA_SECURITY_CREDENTIAL=') for line in env_content):
            env_content.append(f'MPESA_SECURITY_CREDENTIAL={security_credential}\n')
            print("✅ Added MPESA_SECURITY_CREDENTIAL")
        
        # Write updated .env file
        with open(env_file, 'w') as f:
            f.writelines(env_content)
        
        print(f"\n✅ B2C credentials updated in {env_file}")
        
        # Show current configuration
        print("\n📋 Current B2C Configuration:")
        print(f"   - Initiator Name: {initiator_name}")
        print(f"   - Password: {initiator_password}")
        print(f"   - Security Credential: {security_credential[:20]}...")
        print(f"   - Result URL: {os.getenv('MPESA_RESULT_URL', 'http://localhost:5000/api/mpesa/b2c-result')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating {env_file}: {str(e)}")
        return False

def test_b2c_config():
    """Test B2C configuration"""
    
    print("\n🧪 Testing B2C Configuration")
    print("=" * 50)
    
    # Check if credentials are set
    initiator_name = os.getenv('MPESA_INITIATOR_NAME')
    initiator_password = os.getenv('MPESA_INITIATOR_PASSWORD')
    security_credential = os.getenv('MPESA_SECURITY_CREDENTIAL')
    
    if initiator_name and initiator_password and security_credential:
        print("✅ B2C credentials are configured!")
        print(f"   - Initiator Name: {initiator_name}")
        print(f"   - Password: {initiator_password}")
        print(f"   - Security Credential: {security_credential[:20]}...")
        
        # Test M-Pesa service
        try:
            from app import create_app
            from app.mpesa.services import MpesaService
            
            app = create_app()
            with app.app_context():
                mpesa_service = MpesaService()
                print("✅ M-Pesa service initialized successfully!")
                
                # Test B2C configuration
                print(f"   - Base URL: {mpesa_service.base_url}")
                print(f"   - Initiator Name: {mpesa_service.initiator_name}")
                
        except Exception as e:
            print(f"❌ Error testing M-Pesa service: {str(e)}")
            return False
        
        return True
    else:
        print("❌ B2C credentials are missing!")
        print("   Please run this script again to update credentials.")
        return False

if __name__ == "__main__":
    print("🚀 B2C Credentials Update Tool")
    print("=" * 50)
    
    # Update credentials
    success = update_b2c_credentials()
    
    if success:
        # Test configuration
        test_b2c_config()
        
        print("\n🎉 B2C credentials updated successfully!")
        print("\n📝 Next Steps:")
        print("1. Restart your Flask application")
        print("2. Test B2C withdrawal functionality")
        print("3. Run: python test_b2c_withdrawal.py")
    else:
        print("\n❌ Failed to update B2C credentials!")
        print("Please check the error messages above.") 