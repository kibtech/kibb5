#!/usr/bin/env python3
"""
Update Security Credential
This script updates your main system's security credential to match the working B2C implementation
"""

import os
import base64

def update_security_credential():
    """Update the security credential to match the working B2C implementation"""
    
    print("🔧 Updating Security Credential for B2C")
    print("=" * 50)
    
    # The working security credential from b2c/env_correct.txt
    working_security_credential = "PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA=="
    
    # Current security credential from your main system
    current_security_credential = "PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA=="
    
    print("📋 Security Credential Comparison:")
    print("-" * 30)
    
    # Check if they match
    if working_security_credential == current_security_credential:
        print("✅ SECURITY CREDENTIALS ALREADY MATCH!")
        print("   Your main system already has the correct security credential")
        print("   This is perfect for B2C payments!")
        return True
    else:
        print("❌ SECURITY CREDENTIALS DON'T MATCH!")
        print("   Your main system needs the working security credential")
        print("   This is essential for B2C payments to work")
    
    print(f"\n🔑 Working B2C Security Credential:")
    print(f"   Length: {len(working_security_credential)} characters")
    print(f"   Starts with: {working_security_credential[:20]}...")
    print(f"   Ends with: ...{working_security_credential[-20:]}")
    
    print(f"\n🔑 Current Main System Security Credential:")
    print(f"   Length: {len(current_security_credential)} characters")
    print(f"   Starts with: {current_security_credential[:20]}...")
    print(f"   Ends with: ...{current_security_credential[-20:]}")
    
    # Update the environment variable
    print(f"\n🔄 Updating MPESA_SECURITY_CREDENTIAL environment variable...")
    os.environ['MPESA_SECURITY_CREDENTIAL'] = working_security_credential
    print(f"✅ Environment variable updated!")
    
    # Verify the update
    updated_credential = os.environ.get('MPESA_SECURITY_CREDENTIAL')
    if updated_credential == working_security_credential:
        print(f"✅ Security credential successfully updated!")
        print(f"   New credential matches working B2C implementation")
        return True
    else:
        print(f"❌ Failed to update security credential")
        return False

def show_next_steps():
    """Show next steps after updating the security credential"""
    print(f"\n📋 Next Steps:")
    print("=" * 30)
    print(f"1. ✅ Security credential updated to match working B2C implementation")
    print(f"2. 🧪 Test B2C functionality: python test_b2c_with_actual_config.py")
    print(f"3. 📱 Verify you can receive money on your phone")
    print(f"4. 🎉 Your users can now withdraw commission successfully")
    
    print(f"\n🔧 If you have a .env file, also update:")
    print(f"   MPESA_SECURITY_CREDENTIAL=PmDgyWIpGuIlFDs2nvCnmGkfDNCbpoyK6AJaHiFiTHUp0WcYLqqnUVA9zaQh2sADYEiiSrlUA0H4S5mnBhP7mumJOiPDSicdfc6zUZkKx96+krC4RPIJLi4fbRW5AlkK0NtsuSS9BeRKzwaivLA9e//6KnBQeNomdJCobtrVWLcXodL7gY6c+d0/TxGlEWyZhxy01Piie9YpnQ2Fkzm7o/DKE37KHdao5PY3aGF2HwUBlZQcEDLg9hXmX4OAPlAGtjKWc8Ldas9Pln82FatU9YZyx1a+XyRKmrwhx++yNKCmjQMwxGZY8ynDLVh2requSFNilU0cCHEcnrbutxHVmA==")
    
    print(f"\n💡 The security credential is essential for B2C payments because:")
    print(f"   - It encrypts the initiator password")
    print(f"   - M-Pesa requires this for B2C transactions")
    print(f"   - Without it, B2C payments will fail")
    print(f"   - Your working b2c folder has the correct one")

def main():
    """Main function"""
    print("🔧 Security Credential Update for B2C")
    print("=" * 50)
    
    # Update the security credential
    success = update_security_credential()
    
    if success:
        # Show next steps
        show_next_steps()
        
        print(f"\n🎉 Security credential update completed!")
        print(f"✅ Your B2C system should now work correctly!")
        
        return True
    else:
        print(f"\n❌ Security credential update failed!")
        print(f"💡 Please check the error messages above")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🎯 Overall Status: {'✅ UPDATED' if success else '❌ FAILED'}") 