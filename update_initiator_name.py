#!/usr/bin/env python3
"""
Update Initiator Name to KIBTECH
================================
Update the initiator name and regenerate security credential.
"""

import base64
import hashlib

def update_initiator_name():
    """Update initiator name and regenerate security credential"""
    
    print("🔧 Updating Initiator Name to KIBTECH")
    print("=" * 50)
    
    # New credentials
    initiator_name = "KIBTECH"
    initiator_password = "Kibtechceo@2018"
    shortcode = "3547179"
    
    print(f"📋 New Credentials:")
    print(f"   - Initiator Name: {initiator_name}")
    print(f"   - Initiator Password: {initiator_password}")
    print(f"   - Shortcode: {shortcode}")
    
    # Generate new security credentials
    print(f"\n🔐 Generating New Security Credentials:")
    
    # Method 1: Base64 encoding (most common for M-Pesa)
    try:
        encoded_password = base64.b64encode(initiator_password.encode()).decode()
        print(f"   ✅ Base64 Encoded: {encoded_password}")
        
        # Alternative: Encode with shortcode
        combined = f"{shortcode}{initiator_password}"
        encoded_combined = base64.b64encode(combined.encode()).decode()
        print(f"   ✅ Base64 Encoded (with shortcode): {encoded_combined}")
        
    except Exception as e:
        print(f"   ❌ Base64 encoding failed: {e}")
    
    # Method 2: SHA256 hashing
    try:
        sha256_hash = hashlib.sha256(initiator_password.encode()).hexdigest()
        print(f"   ✅ SHA256 Hash: {sha256_hash}")
        
        # Alternative: Hash with shortcode
        combined_hash = hashlib.sha256(f"{shortcode}{initiator_password}".encode()).hexdigest()
        print(f"   ✅ SHA256 Hash (with shortcode): {combined_hash}")
        
    except Exception as e:
        print(f"   ❌ SHA256 hashing failed: {e}")
    
    print(f"\n💡 Recommended Security Credential:")
    print(f"   Use the Base64 encoded password: {encoded_password}")
    
    print(f"\n🔧 To Update Your Config:")
    print(f"   MPESA_INITIATOR_NAME = 'KIBTECH'")
    print(f"   MPESA_SECURITY_CREDENTIAL = '{encoded_password}'")

if __name__ == "__main__":
    update_initiator_name() 