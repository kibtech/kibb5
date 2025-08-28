#!/usr/bin/env python3
"""
Update Initiator Name Environment Variable
==========================================
Update the MPESA_INITIATOR_NAME environment variable to KIBTECH.
"""

import os
import subprocess
import sys

def update_environment_variable():
    """Update the MPESA_INITIATOR_NAME environment variable"""
    
    print("🔧 Updating MPESA_INITIATOR_NAME Environment Variable")
    print("=" * 60)
    
    # Check current environment variable
    current_value = os.environ.get('MPESA_INITIATOR_NAME')
    print(f"📋 Current MPESA_INITIATOR_NAME: {current_value}")
    
    # Set the new value
    new_value = "KIBTECH"
    os.environ['MPESA_INITIATOR_NAME'] = new_value
    
    print(f"✅ Updated MPESA_INITIATOR_NAME to: {new_value}")
    
    # Verify the change
    updated_value = os.environ.get('MPESA_INITIATOR_NAME')
    print(f"🔍 Verified MPESA_INITIATOR_NAME: {updated_value}")
    
    print(f"\n💡 Note: This change is only for the current session.")
    print(f"   To make it permanent, you need to:")
    print(f"   1. Set it in your system environment variables, or")
    print(f"   2. Add it to your .env file, or")
    print(f"   3. Set it before running your scripts")
    
    print(f"\n🔧 To set it permanently in Windows:")
    print(f"   setx MPESA_INITIATOR_NAME KIBTECH")
    
    print(f"\n🔧 To set it for current session only:")
    print(f"   set MPESA_INITIATOR_NAME=KIBTECH")

def set_windows_env_var():
    """Set the environment variable in Windows"""
    try:
        # Set the environment variable using setx (permanent)
        result = subprocess.run(
            ['setx', 'MPESA_INITIATOR_NAME', 'KIBTECH'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            print("✅ Environment variable set permanently using setx")
            print(f"Output: {result.stdout}")
        else:
            print("❌ Failed to set environment variable permanently")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error setting environment variable: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--permanent":
        set_windows_env_var()
    else:
        update_environment_variable() 