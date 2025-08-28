#!/usr/bin/env python3
"""
Fix Production Credentials
This script updates the .env file with the correct production credentials
"""

import os

def fix_production_credentials():
    """Update .env file with correct production credentials"""
    
    print("🔧 Fixing Production Credentials in .env File")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return False
    
    # Read current .env file
    try:
        with open('.env', 'r') as file:
            content = file.read()
        
        print("✅ Read existing .env file")
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    # Production credentials that should be used
    production_credentials = {
        'MPESA_SHORTCODE': '4182541',
        'MPESA_INITIATOR_NAME': 'KIBTECH',
        'MPESA_CONSUMER_KEY': 'kIjdKgFHPcCnAWs3UsDeRUpRDfjgoQ2MAqoSJHM1dGZ2PHNr',
        'MPESA_CONSUMER_SECRET': 'fGkXpABrBgH5w5LGc6sFbrYR243AKEjcA6iyIs1ZgjAHYk3nHtgSOgxUgFY3ASjq',
        'MPESA_INITIATOR_PASSWORD': 'Kibtechceo$2018',
        'MPESA_SECURITY_CREDENTIAL': 'PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA=='
    }
    
    # Split content into lines
    lines = content.split('\n')
    new_lines = []
    
    # Track which variables we've updated
    updated_vars = set()
    
    for line in lines:
        if line.strip() and '=' in line:
            key = line.split('=')[0].strip()
            
            # Check if this is a variable we need to update
            if key in production_credentials:
                new_value = production_credentials[key]
                new_line = f"{key}={new_value}"
                new_lines.append(new_line)
                updated_vars.add(key)
                print(f"✅ Updated {key}: {new_value}")
            else:
                # Keep the line as is
                new_lines.append(line)
        else:
            # Keep empty lines and comments
            new_lines.append(line)
    
    # Check if we missed any variables
    missing_vars = set(production_credentials.keys()) - updated_vars
    if missing_vars:
        print(f"\n⚠️ Some variables not found in .env file: {', '.join(missing_vars)}")
        print("Adding them...")
        for var in missing_vars:
            new_lines.append(f"{var}={production_credentials[var]}")
            print(f"✅ Added {var}: {production_credentials[var]}")
    
    # Write the updated content
    try:
        with open('.env', 'w') as file:
            file.write('\n'.join(new_lines))
        
        print(f"\n✅ Updated .env file with production credentials")
        return True
        
    except Exception as e:
        print(f"❌ Error writing to .env file: {e}")
        return False

def verify_fix():
    """Verify the fix was successful"""
    
    print(f"\n🔍 Verifying the fix...")
    
    try:
        with open('.env', 'r') as file:
            content = file.read()
        
        # Check for the correct values
        if 'MPESA_SHORTCODE=4182541' in content and 'MPESA_INITIATOR_NAME=KIBTECH' in content:
            print("✅ Production credentials verified!")
            return True
        else:
            print("❌ Production credentials not found!")
            return False
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def show_next_steps():
    """Show next steps after fixing the credentials"""
    print(f"\n📋 Next Steps:")
    print("=" * 30)
    print(f"1. ✅ Production credentials updated in .env file")
    print(f"2. 🔄 Restart your terminal/IDE to load new environment variables")
    print(f"3. 🧪 Test B2C with production credentials: python test_b2c_standalone.py")
    print(f"4. 📱 Verify you can receive money on your phone")
    print(f"5. 🎉 Your users can now withdraw commission with real money!")
    
    print(f"\n💡 Important:")
    print(f"   - Environment variables are loaded when the terminal starts")
    print(f"   - You need to restart your terminal after changing .env file")
    print(f"   - This will now use REAL production credentials")
    print(f"   - Real money will be transferred!")

def main():
    """Main function"""
    print("🔧 Fix Production Credentials")
    print("=" * 50)
    
    # Fix the credentials
    if fix_production_credentials():
        # Verify the fix
        if verify_fix():
            show_next_steps()
            print(f"\n🎉 Production credentials fixed successfully!")
            print(f"✅ Your B2C system will now use real production credentials!")
            return True
        else:
            print(f"\n❌ Credential verification failed!")
            return False
    else:
        print(f"\n❌ Failed to fix production credentials!")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🎯 Overall Status: {'✅ FIXED' if success else '❌ FAILED'}") 