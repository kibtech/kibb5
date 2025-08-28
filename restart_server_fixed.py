#!/usr/bin/env python3
"""
Restart Server with All Fixes
This script will restart the Flask server with all CORS and login fixes applied
"""

import os
import sys
import subprocess
import time
import signal

def kill_flask_processes():
    """Kill any existing Flask processes"""
    print("🔄 Stopping existing Flask processes...")
    
    try:
        if os.name == 'nt':  # Windows
            # Kill Python processes that might be running Flask
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True)
            subprocess.run(['taskkill', '/f', '/im', 'pythonw.exe'], capture_output=True)
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'python.*run.py'], capture_output=True)
            subprocess.run(['pkill', '-f', 'flask'], capture_output=True)
        
        time.sleep(3)  # Wait for processes to stop
        print("✅ Existing processes stopped")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not stop all processes: {e}")

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Flask server with CORS fixes...")
    print("=" * 50)
    print("📋 Server Information:")
    print("   URL: http://localhost:5000")
    print("   Admin Portal: http://localhost:5000/admin")
    print("   Alternative: http://127.0.0.1:5000/admin")
    print("\n🔐 Login Credentials:")
    print("   Email: kibtechc@gmail.com")
    print("   Password: Kibtechceo@2018")
    print("\n⚙️ CORS Fixes Applied:")
    print("   ✅ Added localhost:5000 to allowed origins")
    print("   ✅ Added 127.0.0.1:5000 to allowed origins")
    print("   ✅ Added CORS headers to admin login route")
    print("   ✅ Added OPTIONS route for preflight requests")
    
    print("\n🔄 Starting server...")
    print("   Press Ctrl+C to stop the server")
    print("   " + "="*50)
    
    try:
        # Start the server
        subprocess.run([sys.executable, 'run.py'])
        
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🔧 Flask Server Restart with CORS Fixes")
    print("=" * 50)
    
    # Kill existing processes
    kill_flask_processes()
    
    # Start server
    start_server()

if __name__ == '__main__':
    main() 