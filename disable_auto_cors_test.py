#!/usr/bin/env python3
"""
Disable Auto CORS Test
This script can disable the automatic CORS test if needed
"""

def disable_auto_cors_test():
    """Disable the automatic CORS test"""
    print("🔧 Disabling Auto CORS Test...")
    print("=" * 40)
    
    # Read the current app/__init__.py file
    with open('app/__init__.py', 'r') as f:
        content = f.read()
    
    # Comment out the auto test call
    if 'auto_test_cors()' in content:
        content = content.replace('auto_test_cors()', '# auto_test_cors()  # Disabled')
        print("✅ Auto CORS test disabled")
    else:
        print("ℹ️ Auto CORS test already disabled or not found")
    
    # Write back the modified content
    with open('app/__init__.py', 'w') as f:
        f.write(content)
    
    print("\n📋 Auto CORS test has been disabled.")
    print("To re-enable it, edit app/__init__.py and uncomment the line:")
    print("   # auto_test_cors()  # Disabled")
    print("   auto_test_cors()")

def enable_auto_cors_test():
    """Re-enable the automatic CORS test"""
    print("🔧 Re-enabling Auto CORS Test...")
    print("=" * 40)
    
    # Read the current app/__init__.py file
    with open('app/__init__.py', 'r') as f:
        content = f.read()
    
    # Uncomment the auto test call
    if '# auto_test_cors()  # Disabled' in content:
        content = content.replace('# auto_test_cors()  # Disabled', 'auto_test_cors()')
        print("✅ Auto CORS test re-enabled")
    else:
        print("ℹ️ Auto CORS test already enabled or not found")
    
    # Write back the modified content
    with open('app/__init__.py', 'w') as f:
        f.write(content)
    
    print("\n📋 Auto CORS test has been re-enabled.")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'enable':
        enable_auto_cors_test()
    else:
        disable_auto_cors_test() 