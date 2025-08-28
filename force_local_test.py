#!/usr/bin/env python3
"""
Force Local Testing
This script forces the auto CORS test to use local testing
"""

import os
import subprocess
import sys

def force_local_test():
    """Force local testing by setting FORCE_LOCAL environment variable"""
    print("🏠 Forcing Local Testing")
    print("=" * 30)
    
    # Set environment variable to force local testing
    os.environ['FORCE_LOCAL'] = 'true'
    
    print("✅ FORCE_LOCAL=true set")
    print("🔧 Auto CORS test will use local testing regardless of ENVIRONMENT setting")
    
    print("\n🎯 Starting server with local testing...")
    print("   This will test localhost URLs even if ENVIRONMENT=production")
    
    try:
        # Start the server with the environment variable
        subprocess.run([sys.executable, 'run.py'], env=os.environ)
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    force_local_test() 