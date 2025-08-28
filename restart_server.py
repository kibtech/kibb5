#!/usr/bin/env python3
"""
Script to restart the Flask server
"""

import os
import signal
import subprocess
import time
import sys

def restart_server():
    """Restart the Flask server"""
    print("🔄 Restarting Flask server...")
    
    # Kill any existing Python processes running the server
    try:
        # On Windows, we need to find and kill the process
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                              capture_output=True, text=True)
        
        if 'python.exe' in result.stdout:
            print("⚠️  Found running Python processes. Please stop the server manually:")
            print("   Press Ctrl+C in the terminal where the server is running")
            print("   Then run: python run.py")
            return False
    except Exception as e:
        print(f"Error checking processes: {e}")
    
    # Start the server
    try:
        print("🚀 Starting Flask server...")
        subprocess.run([sys.executable, 'run.py'])
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == '__main__':
    restart_server() 