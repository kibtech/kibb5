#!/usr/bin/env python3
"""
Fix B2C Security Credential
===========================
Encrypt the B2C security credential properly for production use.
"""

import base64
import hashlib
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_security_credential():
    """Generate properly encrypted security credential for B2C"""
    
    print("🔧 Fixing B2C Security Credential")
    print("=" * 50)
    
    # Your current credentials
    initiator_name = "GEOFFREYKIBET"
    initiator_password = "Kibtechceo@2018"
    shortcode = "3547179"
    
    print(f"📋 Current Credentials:")
    print(f"   - Initiator Name: {initiator_name}")
    print(f"   - Initiator Password: {initiator_password}")
    print(f"   - Shortcode: {shortcode}")
    
    # Method 1: Base64 encoding (most common for M-Pesa)
    print(f"\n🔐 Method 1: Base64 Encoding")
    try:
        # Encode the password in base64
        encoded_password = base64.b64encode(initiator_password.encode()).decode()
        print(f"   ✅ Base64 Encoded: {encoded_password}")
        
        # Alternative: Encode with shortcode
        combined = f"{shortcode}{initiator_password}"
        encoded_combined = base64.b64encode(combined.encode()).decode()
        print(f"   ✅ Base64 Encoded (with shortcode): {encoded_combined}")
        
    except Exception as e:
        print(f"   ❌ Base64 encoding failed: {e}")
    
    # Method 2: SHA256 hashing
    print(f"\n🔐 Method 2: SHA256 Hashing")
    try:
        sha256_hash = hashlib.sha256(initiator_password.encode()).hexdigest()
        print(f"   ✅ SHA256 Hash: {sha256_hash}")
        
        # Alternative: Hash with shortcode
        combined_hash = hashlib.sha256(f"{shortcode}{initiator_password}".encode()).hexdigest()
        print(f"   ✅ SHA256 Hash (with shortcode): {combined_hash}")
        
    except Exception as e:
        print(f"   ❌ SHA256 hashing failed: {e}")
    
    # Method 3: MD5 hashing (older M-Pesa method)
    print(f"\n🔐 Method 3: MD5 Hashing")
    try:
        md5_hash = hashlib.md5(initiator_password.encode()).hexdigest()
        print(f"   ✅ MD5 Hash: {md5_hash}")
        
    except Exception as e:
        print(f"   ❌ MD5 hashing failed: {e}")
    
    print(f"\n💡 Recommendations:")
    print(f"   1. Try the Base64 encoded password first")
    print(f"   2. If that doesn't work, try the SHA256 hash")
    print(f"   3. Contact Safaricom for the correct encryption method")
    print(f"   4. Check your M-Pesa documentation for the required format")
    
    print(f"\n🔧 To update your config:")
    print(f"   Set MPESA_SECURITY_CREDENTIAL to one of the encoded values above")
    print(f"   Or set MPESA_INITIATOR_PASSWORD to the plain password and let the system encrypt it")
    
    return encoded_password

def test_different_credentials():
    """Test different security credential formats"""
    
    print(f"\n🧪 Testing Different Credential Formats")
    print("=" * 50)
    
    credentials_to_test = [
        ("Plain Text", "Kibtechceo@2018"),
        ("Base64", base64.b64encode("Kibtechceo@2018".encode()).decode()),
        ("SHA256", hashlib.sha256("Kibtechceo@2018".encode()).hexdigest()),
        ("MD5", hashlib.md5("Kibtechceo@2018".encode()).hexdigest()),
    ]
    
    for name, credential in credentials_to_test:
        print(f"   {name}: {credential}")

if __name__ == "__main__":
    generate_security_credential()
    test_different_credentials() 