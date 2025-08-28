#!/usr/bin/env python3
"""
Script to build and serve the React frontend from Flask backend
"""

import os
import subprocess
import shutil
import sys

def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("=== Building and Serving Frontend from Backend ===")
    print()
    
    # Check if frontend directory exists
    if not os.path.exists("frontend"):
        print("❌ frontend directory not found!")
        print("Please ensure you're in the project root directory")
        return
    
    # Step 1: Install frontend dependencies
    if not run_command("npm install", "Installing frontend dependencies", cwd="frontend"):
        return
    
    # Step 2: Build the frontend
    if not run_command("npm run build", "Building frontend for production", cwd="frontend"):
        return
    
    # Step 3: Copy build files to backend static directory
    print("🔄 Copying build files to backend...")
    try:
        # Create static directory if it doesn't exist
        os.makedirs("static", exist_ok=True)
        
        # Copy build files
        if os.path.exists("frontend/build"):
            # Remove existing static files
            if os.path.exists("static"):
                shutil.rmtree("static")
            
            # Copy new build files
            shutil.copytree("frontend/build", "static")
            print("✅ Build files copied to static directory")
        else:
            print("❌ Build directory not found!")
            return
    except Exception as e:
        print(f"❌ Error copying build files: {e}")
        return
    
    print()
    print("✅ Frontend built and ready to serve!")
    print()
    print("Next steps:")
    print("1. Update your Flask app to serve static files")
    print("2. Restart your Flask application")
    print("3. Access your app at the root URL")

if __name__ == "__main__":
    main() 