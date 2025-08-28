#!/usr/bin/env python3
"""
Update Callback URLs for Testing
This script updates the callback URLs to use ngrok for testing
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_callback_urls():
    """Update callback URLs to use ngrok for testing"""
    print("🔧 Update Callback URLs for Testing")
    print("=" * 50)
    
    # Ngrok URL
    ngrok_url = "https://65db561a00a0.ngrok-free.app"
    
    # New callback URLs
    new_result_url = f"{ngrok_url}/api/mpesa/b2c-result"
    new_timeout_url = f"{ngrok_url}/api/mpesa/timeout"
    new_callback_url = f"{ngrok_url}/api/mpesa/callback"
    
    print(f"🌐 Ngrok URL: {ngrok_url}")
    print(f"📋 New Callback URLs:")
    print(f"   Result URL: {new_result_url}")
    print(f"   Timeout URL: {new_timeout_url}")
    print(f"   Callback URL: {new_callback_url}")
    
    # Read current .env file
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"❌ .env file not found")
        return False
    
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update callback URLs
    updated = False
    new_lines = []
    
    for line in lines:
        if line.startswith('MPESA_RESULT_URL='):
            new_lines.append(f'MPESA_RESULT_URL={new_result_url}\n')
            updated = True
            print(f"✅ Updated MPESA_RESULT_URL")
        elif line.startswith('MPESA_TIMEOUT_URL='):
            new_lines.append(f'MPESA_TIMEOUT_URL={new_timeout_url}\n')
            updated = True
            print(f"✅ Updated MPESA_TIMEOUT_URL")
        elif line.startswith('MPESA_CALLBACK_URL='):
            new_lines.append(f'MPESA_CALLBACK_URL={new_callback_url}\n')
            updated = True
            print(f"✅ Updated MPESA_CALLBACK_URL")
        else:
            new_lines.append(line)
    
    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(new_lines)
    
    if updated:
        print(f"\n✅ Callback URLs updated successfully!")
        print(f"🔄 Please restart your Flask application to load the new URLs")
        print(f"🧪 Now your B2C callbacks will go to ngrok for testing")
    else:
        print(f"\n⚠️ No callback URLs found to update")
    
    return True

if __name__ == "__main__":
    update_callback_urls() 