#!/usr/bin/env python3
"""
Complete script to remove email verification requirements from user registration and password reset.
This will:
1. Update the User model to default email_verified to True
2. Remove email verification checks from auth routes
3. Create a migration script for the database
"""

import os
import re

def update_user_model():
    """Update the User model to default email_verified to True"""
    try:
        model_file = "app/models.py"
        
        if not os.path.exists(model_file):
            print(f"❌ Model file not found: {model_file}")
            return False
        
        # Read the current model file
        with open(model_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the User model email_verified default
        old_line = "email_verified = db.Column(db.Boolean, default=False)"
        new_line = "email_verified = db.Column(db.Boolean, default=True)"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
            print("✅ Updated User model email_verified default to True")
        else:
            print("⚠️  User model email_verified line not found")
        
        # Update the AdminUser model email_verified default
        old_admin_line = "email_verified = db.Column(db.Boolean, default=False)"
        new_admin_line = "email_verified = db.Column(db.Boolean, default=True)"
        
        if old_admin_line in content:
            content = content.replace(old_admin_line, new_admin_line)
            print("✅ Updated AdminUser model email_verified default to True")
        else:
            print("⚠️  AdminUser model email_verified line not found")
        
        # Write the updated content back
        with open(model_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating model file: {e}")
        return False

def update_auth_routes():
    """Remove email verification checks from auth routes"""
    auth_files = [
        "app/auth/routes.py"
    ]
    
    for auth_file in auth_files:
        if not os.path.exists(auth_file):
            print(f"⚠️  Auth file not found: {auth_file}")
            continue
            
        try:
            # Read the current file
            with open(auth_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove email verification checks
            changes_made = False
            
            # Pattern to find and remove email verification blocks
            # This regex finds if statements that check email_verified and removes them
            email_verification_pattern = r'\s*if\s+(?:not\s+)?user\.email_verified[^:]*:\s*\n(?:\s+.*\n)*'
            
            # Find all matches
            matches = re.finditer(email_verification_pattern, content)
            for match in matches:
                print(f"✅ Found email verification check in {auth_file}")
                changes_made = True
            
            # Remove the email verification checks
            content = re.sub(email_verification_pattern, '', content)
            
            # Also remove any remaining email_verified=False filters
            content = re.sub(r'email_verified\s*=\s*False', 'email_verified=True', content)
            content = re.sub(r'email_verified\s*=\s*False', 'email_verified=True', content)
            
            if changes_made:
                # Write the updated content back
                with open(auth_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Updated {auth_file}")
            
        except Exception as e:
            print(f"❌ Error updating {auth_file}: {e}")

def create_migration_script():
    """Create a database migration script to update existing users"""
    migration_script = """-- Migration script to set all users as email verified
-- Run this in your database to update existing users

-- For PostgreSQL:
UPDATE users SET email_verified = TRUE;
UPDATE admin_users SET email_verified = TRUE;

-- For SQLite:
-- UPDATE users SET email_verified = 1;
-- UPDATE admin_users SET email_verified = 1;

-- Verify the changes
SELECT COUNT(*) as total_users, 
       COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_users
FROM users;

SELECT COUNT(*) as total_admin_users, 
       COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_admin_users
FROM admin_users;
"""
    
    with open('migrate_email_verification.sql', 'w') as f:
        f.write(migration_script)
    
    print("✅ Created migration script: migrate_email_verification.sql")

def create_batch_script():
    """Create a batch script to run the migration"""
    batch_script = """@echo off
echo Starting email verification removal process...

echo.
echo Step 1: Running Python script...
python remove_email_verification_complete.py

echo.
echo Step 2: Running database migration...
echo Please run the SQL commands in migrate_email_verification.sql in your database

echo.
echo Step 3: Restart your Flask application
echo The email verification requirement has been removed!

pause
"""
    
    with open('remove_email_verification.bat', 'w') as f:
        f.write(batch_script)
    
    print("✅ Created batch script: remove_email_verification.bat")

def main():
    """Main function to remove email verification requirements"""
    print("🚀 Starting complete email verification removal process...")
    print("=" * 60)
    
    # Step 1: Update User model
    print("\n1️⃣ Updating User model...")
    if update_user_model():
        print("✅ User model updated successfully")
    else:
        print("❌ Failed to update User model")
    
    # Step 2: Update auth routes
    print("\n2️⃣ Updating authentication routes...")
    update_auth_routes()
    
    # Step 3: Create migration script
    print("\n3️⃣ Creating migration script...")
    create_migration_script()
    
    # Step 4: Create batch script
    print("\n4️⃣ Creating batch script...")
    create_batch_script()
    
    print("\n" + "=" * 60)
    print("✅ Complete email verification removal process completed!")
    print("\n📋 What was done:")
    print("   • Modified User model to default email_verified to True")
    print("   • Removed email verification checks from auth routes")
    print("   • Created migration script for manual database updates")
    print("   • Created batch script for easy execution")
    
    print("\n⚠️  Important notes:")
    print("   • Users can now register and reset passwords without email verification")
    print("   • You need to run the migration script to update existing users")
    print("   • You may need to restart your Flask application")
    
    print("\n🔄 Next steps:")
    print("   1. Run: remove_email_verification.bat")
    print("   2. Execute the SQL commands in migrate_email_verification.sql")
    print("   3. Restart your Flask application")
    print("   4. Test user registration and password reset")

if __name__ == "__main__":
    main() 