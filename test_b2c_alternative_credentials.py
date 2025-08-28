#!/usr/bin/env python3
"""
Test B2C with Alternative Security Credentials
==============================================
Test different security credential formats to find the correct one.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import requests
import base64
import hashlib
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_b2c_with_different_credentials():
    """Test B2C with different security credential formats"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing B2C with Different Security Credentials")
        print("=" * 60)
        
        # Test credentials
        initiator_name = "GEOFFREYKIBET"
        initiator_password = "Kibtechceo@2018"
        shortcode = "3547179"
        
        # Different credential formats to test
        credentials_to_test = [
            ("Plain Text", initiator_password),
            ("Base64", base64.b64encode(initiator_password.encode()).decode()),
            ("SHA256", hashlib.sha256(initiator_password.encode()).hexdigest()),
            ("MD5", hashlib.md5(initiator_password.encode()).hexdigest()),
            ("Base64 with Shortcode", base64.b64encode(f"{shortcode}{initiator_password}".encode()).decode()),
            ("SHA256 with Shortcode", hashlib.sha256(f"{shortcode}{initiator_password}".encode()).hexdigest()),
        ]
        
        for i, (name, credential) in enumerate(credentials_to_test, 1):
            print(f"\n{i}. Testing {name} credential...")
            print(f"   Credential: {credential}")
            
            try:
                # Get access token
                from app.mpesa.services import MpesaService
                mpesa_service = MpesaService()
                
                # Temporarily override security credential
                original_credential = app.config.get('MPESA_SECURITY_CREDENTIAL')
                app.config['MPESA_SECURITY_CREDENTIAL'] = credential
                
                access_token = mpesa_service.get_access_token()
                if not access_token:
                    print(f"   ❌ Failed to get access token")
                    continue
                
                # Test B2C with small amount
                test_amount = 1
                test_phone = "254712591937"
                
                b2c_response = mpesa_service.b2c_payment(
                    phone_number=test_phone,
                    amount=test_amount,
                    remarks=f"Test {name} credential"
                )
                
                print(f"   Response: {b2c_response}")
                
                if 'ConversationID' in b2c_response:
                    print(f"   ✅ Success! Conversation ID: {b2c_response['ConversationID']}")
                    if 'ResponseDescription' in b2c_response:
                        desc = b2c_response['ResponseDescription']
                        if 'otp' not in desc.lower() and 'passcode' not in desc.lower():
                            print(f"   🎉 No OTP required! This might be the correct format!")
                            break
                        else:
                            print(f"   ⚠️  Still requires OTP")
                elif 'error' in b2c_response:
                    print(f"   ❌ Error: {b2c_response['error']}")
                else:
                    print(f"   ⚠️  Unexpected response")
                
                # Restore original credential
                app.config['MPESA_SECURITY_CREDENTIAL'] = original_credential
                
            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")
                # Restore original credential
                app.config['MPESA_SECURITY_CREDENTIAL'] = original_credential
        
        print(f"\n💡 Summary:")
        print(f"   - If all formats require OTP, it's a business account issue")
        print(f"   - If one format works without OTP, that's the correct format")
        print(f"   - Contact Safaricom to disable OTP requirement for B2C")

if __name__ == "__main__":
    test_b2c_with_different_credentials() 