#!/usr/bin/env python3
"""
Quick fix for Scalingo deployment - adds missing dependencies
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_status():
    """Check if we're in a git repository"""
    try:
        subprocess.run(["git", "status"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=== Quick Scalingo Fix ===")
    print()
    
    # Check if we're in a git repository
    if not check_git_status():
        print("❌ Not in a git repository!")
        print("Please run this script from your project directory")
        return
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return
    
    # Check if cryptography is in requirements.txt
    with open("requirements.txt", "r") as f:
        content = f.read()
        if "cryptography" not in content:
            print("❌ cryptography package not found in requirements.txt!")
            print("Please ensure requirements.txt contains: cryptography==41.0.7")
            return
    
    print("✅ requirements.txt contains cryptography package")
    print()
    
    # Step 1: Add requirements.txt to git
    if not run_command("git add requirements.txt", "Adding requirements.txt to git"):
        return
    
    # Step 2: Commit changes
    if not run_command('git commit -m "Add missing cryptography dependency for MPesa services"', "Committing changes"):
        return
    
    # Step 3: Try to push to Scalingo
    print("🔄 Attempting to push to Scalingo...")
    print("Note: You may need to configure your Scalingo remote first")
    print()
    
    # Check if Scalingo remote exists
    try:
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        if "scalingo" in result.stdout.lower():
            if run_command("git push scalingo main", "Pushing to Scalingo"):
                print("✅ Successfully pushed to Scalingo!")
                print("Your app should now deploy with the missing dependencies")
            else:
                print("❌ Failed to push to Scalingo")
                print("You may need to:")
                print("1. Configure your Scalingo remote")
                print("2. Use Scalingo CLI: scalingo --app your-app-name deploy")
        else:
            print("⚠️  No Scalingo remote found")
            print("You can:")
            print("1. Add Scalingo remote: git remote add scalingo <your-scalingo-git-url>")
            print("2. Use Scalingo CLI: scalingo --app your-app-name deploy")
            print("3. Deploy manually through Scalingo dashboard")
    except Exception as e:
        print(f"❌ Error checking git remotes: {e}")
    
    print()
    print("=== Next Steps ===")
    print("1. If push was successful, check your Scalingo dashboard")
    print("2. Monitor the deployment logs")
    print("3. The app should start without the ModuleNotFoundError")

if __name__ == "__main__":
    main() 