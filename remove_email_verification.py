#!/usr/bin/env python3
"""
Remove email verification requirements from user registration and password reset
"""

import os
import sys

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

def main():
    """Main function to remove email verification requirements"""
    print("🚀 Starting email verification removal process...")
    print("=" * 60)
    
    # Step 1: Update User model
    print("\n1️⃣ Updating User model...")
    if update_user_model():
        print("✅ User model updated successfully")
    else:
        print("❌ Failed to update User model")
    
    # Step 2: Create migration script
    print("\n2️⃣ Creating migration script...")
    create_migration_script()
    
    print("\n" + "=" * 60)
    print("✅ Email verification removal process completed!")
    print("\n📋 What was done:")
    print("   • Modified User model to default email_verified to True")
    print("   • Created migration script for manual database updates")
    
    print("\n⚠️  Important notes:")
    print("   • Users can now register and reset passwords without email verification")
    print("   • You need to run the migration script to update existing users")
    print("   • You may need to restart your Flask application")
    
    print("\n🔄 Next steps:")
    print("   1. Run the migration script: migrate_email_verification.sql")
    print("   2. Restart your Flask application")
    print("   3. Test user registration and password reset")

if __name__ == "__main__":
    main() 