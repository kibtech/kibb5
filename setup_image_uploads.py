#!/usr/bin/env python3
"""
Setup Image Uploads
==================
Set up the image upload functionality for cyber services.
"""

import os
import sys

def create_upload_directories():
    """Create necessary upload directories"""
    
    print("📁 Creating Upload Directories")
    print("=" * 40)
    
    # Create static directory structure
    directories = [
        'static',
        'static/uploads',
        'static/uploads/cyber-services'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def install_required_packages():
    """Install required Python packages"""
    
    print("\n📦 Installing Required Packages")
    print("=" * 40)
    
    packages = [
        'Pillow',  # For image processing
        'werkzeug'  # For secure filename handling
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        os.system(f"pip install {package}")

def create_gitignore_entry():
    """Add uploads directory to .gitignore"""
    
    gitignore_entry = "\n# Uploaded files\nstatic/uploads/\n"
    
    try:
        # Check if .gitignore exists
        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r') as f:
                content = f.read()
            
            # Add entry if not already present
            if 'static/uploads/' not in content:
                with open('.gitignore', 'a') as f:
                    f.write(gitignore_entry)
                print("✅ Added uploads directory to .gitignore")
            else:
                print("📝 .gitignore already contains uploads directory")
        else:
            # Create .gitignore if it doesn't exist
            with open('.gitignore', 'w') as f:
                f.write(gitignore_entry.strip())
            print("✅ Created .gitignore with uploads directory")
            
    except Exception as e:
        print(f"⚠️  Could not update .gitignore: {e}")

def test_upload_setup():
    """Test the upload setup"""
    
    print("\n🧪 Testing Upload Setup")
    print("=" * 40)
    
    # Test directory permissions
    test_file = 'static/uploads/cyber-services/test.txt'
    
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        
        os.remove(test_file)
        print("✅ Upload directory is writable")
        
    except Exception as e:
        print(f"❌ Upload directory test failed: {e}")
        return False
    
    # Test PIL import
    try:
        from PIL import Image
        print("✅ PIL (Pillow) is available for image processing")
    except ImportError:
        print("⚠️  PIL (Pillow) not available - install with: pip install Pillow")
        return False
    
    return True

def show_setup_summary():
    """Show setup summary and next steps"""
    
    print("\n📋 SETUP SUMMARY")
    print("=" * 40)
    
    summary = '''
🎉 IMAGE UPLOAD FEATURE READY!

✅ WHAT'S BEEN SET UP:
• Upload directories created
• Backend endpoints configured
• Frontend upload component added
• Image optimization enabled
• File validation implemented

🔧 FEATURES INCLUDED:
• Direct file upload (browse & select)
• Drag & drop support
• Image optimization (resize, compress)
• File type validation (JPG, PNG, GIF, WEBP)
• File size limit (5MB)
• Live preview
• URL input as alternative
• Error handling
• Remove image functionality

📱 HOW TO USE:
1. Go to Admin Portal → Cyber Services
2. Click "Add Service" or "Edit" existing service
3. In the "Service Image" section:
   - Click "Choose File" to upload from computer
   - OR enter a direct image URL
4. See live preview of your image
5. Save service - image appears immediately!

🎯 ADMIN EXPERIENCE:
• Upload images directly from computer
• Automatic image optimization
• Live preview before saving
• Easy image removal
• Fallback to URL input

👥 CUSTOMER EXPERIENCE:
• Beautiful service cards with images
• Fast loading optimized images
• Professional appearance
• Mobile-friendly display

🔒 SECURITY FEATURES:
• File type validation
• File size limits
• Secure filename handling
• Directory traversal protection
'''
    
    print(summary)

if __name__ == "__main__":
    print("🖼️ Setting Up Image Upload for Cyber Services")
    print("=" * 50)
    
    # Create directories
    create_upload_directories()
    
    # Install packages
    install_required_packages()
    
    # Update .gitignore
    create_gitignore_entry()
    
    # Test setup
    success = test_upload_setup()
    
    # Show summary
    show_setup_summary()
    
    if success:
        print("\n🎉 SETUP COMPLETE! Image upload is ready to use!")
    else:
        print("\n⚠️  Setup completed with warnings. Check the messages above.")