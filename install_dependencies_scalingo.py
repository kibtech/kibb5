#!/usr/bin/env python3
"""
Install missing dependencies directly on Scalingo
"""

import subprocess
import sys

def run_scalingo_command(command, description):
    """Run a Scalingo CLI command"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("=== Installing Missing Dependencies on Scalingo ===")
    print()
    
    # Check if Scalingo CLI is available
    try:
        subprocess.run(["scalingo", "--version"], check=True, capture_output=True)
        print("✅ Scalingo CLI found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Scalingo CLI not found!")
        print("Please install Scalingo CLI first:")
        print("https://doc.scalingo.com/platform/cli/installation")
        return
    
    print()
    print("Installing missing dependencies...")
    print()
    
    # Install cryptography package
    if run_scalingo_command("scalingo --app kibtech run pip install cryptography==41.0.7", "Installing cryptography"):
        print("✅ cryptography package installed")
    else:
        print("❌ Failed to install cryptography")
        return
    
    # Install sib_api_v3_sdk package (in case it's missing)
    if run_scalingo_command("scalingo --app kibtech run pip install sib_api_v3_sdk==7.5.0", "Installing sib_api_v3_sdk"):
        print("✅ sib_api_v3_sdk package installed")
    else:
        print("❌ Failed to install sib_api_v3_sdk")
        return
    
    print()
    print("=== Restarting Application ===")
    
    # Restart the application
    if run_scalingo_command("scalingo --app kibtech restart", "Restarting application"):
        print("✅ Application restarted successfully")
        print()
        print("Your application should now start without the ModuleNotFoundError!")
        print("Check the logs to verify: scalingo --app kibtech logs")
    else:
        print("❌ Failed to restart application")

if __name__ == "__main__":
    main() 