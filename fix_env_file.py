#!/usr/bin/env python3
"""
Fix .env File
This script fixes the .env file by adding the missing MPESA_SECURITY_CREDENTIAL
"""

import os

def fix_env_file():
    """Fix the .env file by adding the missing security credential"""
    
    print("🔧 Fixing .env File")
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
    
    # Check if security credential is missing
    if 'MPESA_SECURITY_CREDENTIAL=' not in content:
        print("❌ MPESA_SECURITY_CREDENTIAL is missing from .env file")
        
        # Add the security credential
        security_credential_line = '\nMPESA_SECURITY_CREDENTIAL=PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA==\n'
        
        # Add it after MPESA_INITIATOR_PASSWORD
        if 'MPESA_INITIATOR_PASSWORD=' in content:
            # Find the line after MPESA_INITIATOR_PASSWORD
            lines = content.split('\n')
            new_lines = []
            
            for line in lines:
                new_lines.append(line)
                if line.startswith('MPESA_INITIATOR_PASSWORD='):
                    new_lines.append('MPESA_SECURITY_CREDENTIAL=PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA==')
            
            new_content = '\n'.join(new_lines)
        else:
            # Add at the end
            new_content = content + '\nMPESA_SECURITY_CREDENTIAL=PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA==\n'
        
        # Write the updated content
        try:
            with open('.env', 'w') as file:
                file.write(new_content)
            
            print("✅ Added MPESA_SECURITY_CREDENTIAL to .env file")
            return True
            
        except Exception as e:
            print(f"❌ Error writing to .env file: {e}")
            return False
    
    else:
        print("✅ MPESA_SECURITY_CREDENTIAL already exists in .env file")
        return True

def verify_env_file():
    """Verify the .env file has all required variables"""
    
    print(f"\n🔍 Verifying .env file...")
    
    try:
        with open('.env', 'r') as file:
            content = file.read()
        
        required_vars = [
            'MPESA_CONSUMER_KEY=',
            'MPESA_CONSUMER_SECRET=',
            'MPESA_SHORTCODE=',
            'MPESA_PASSKEY=',
            'MPESA_INITIATOR_NAME=',
            'MPESA_INITIATOR_PASSWORD=',
            'MPESA_SECURITY_CREDENTIAL=',
            'MPESA_BASE_URL='
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in content:
                missing_vars.append(var.replace('=', ''))
        
        if missing_vars:
            print(f"❌ Missing variables: {', '.join(missing_vars)}")
            return False
        else:
            print("✅ All required variables are present in .env file")
            return True
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def show_next_steps():
    """Show next steps after fixing the .env file"""
    print(f"\n📋 Next Steps:")
    print("=" * 30)
    print(f"1. ✅ .env file fixed with security credential")
    print(f"2. 🔄 Restart your terminal/IDE to load new environment variables")
    print(f"3. 🧪 Test B2C functionality: python test_b2c_with_actual_config.py")
    print(f"4. 📱 Verify you can receive money on your phone")
    print(f"5. 🎉 Your users can now withdraw commission successfully")
    
    print(f"\n💡 Important:")
    print(f"   - Environment variables are loaded when the terminal starts")
    print(f"   - You need to restart your terminal after changing .env file")
    print(f"   - The security credential is essential for B2C payments")

def main():
    """Main function"""
    print("🔧 Fix .env File")
    print("=" * 50)
    
    # Fix the .env file
    if fix_env_file():
        # Verify the fix
        if verify_env_file():
            show_next_steps()
            print(f"\n🎉 .env file fixed successfully!")
            print(f"✅ Your B2C system should now work correctly!")
            return True
        else:
            print(f"\n❌ .env file verification failed!")
            return False
    else:
        print(f"\n❌ Failed to fix .env file!")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🎯 Overall Status: {'✅ FIXED' if success else '❌ FAILED'}") 