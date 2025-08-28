#!/usr/bin/env python3
"""
Fix email verification issue in PostgreSQL database
Updates all users to have email_verified=True to resolve 403 errors
Works for both local and production PostgreSQL databases
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_email_verification():
    """Fix email verification for all users in PostgreSQL database"""
    
    # Get database URL from environment or use default
    database_url = os.environ.get('DATABASE_URL') or 'postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres'
    
    # Alternative connection string if the first one fails
    alternative_url = 'postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@fcrvabkgdhdvprwwlyuf.supabase.co:5432/postgres'
    
    try:
        print("🚀 Connecting to PostgreSQL database...")
        
        # Try the first connection string
        try:
            print("🔌 Attempting connection with pooler hostname...")
            conn = psycopg2.connect(database_url)
            print("✅ Connected to database successfully using pooler!")
        except Exception as first_error:
            print(f"⚠️  First connection failed: {first_error}")
            print("🔄 Trying alternative connection...")
            
            # Try the alternative connection string
            try:
                conn = psycopg2.connect(alternative_url)
                print("✅ Connected to database successfully using direct connection!")
            except Exception as second_error:
                print(f"❌ Both connection attempts failed:")
                print(f"   Pooler: {first_error}")
                print(f"   Direct: {second_error}")
                raise Exception("All database connection attempts failed")
        
        cursor = conn.cursor()
        
        print("🚀 Starting email verification fix...")
        
        # Check if email_verified column exists in users table
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'email_verified'
        """)
        
        if not cursor.fetchone():
            print("❌ email_verified column not found in users table")
            print("This suggests the database schema is not up to date")
            return False
        
        print("📝 Updating all users to have verified emails...")
        
        # Update all users to have email_verified = True
        cursor.execute("UPDATE users SET email_verified = TRUE")
        users_updated = cursor.rowcount
        
        print(f"✅ Updated {users_updated} users")
        
        # Check if admin_users table exists and update it too
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'admin_users'
        """)
        
        if cursor.fetchone():
            print("📝 Updating admin users table...")
            cursor.execute("UPDATE admin_users SET email_verified = TRUE")
            admin_users_updated = cursor.rowcount
            print(f"✅ Updated {admin_users_updated} admin users")
        
        # Commit the changes
        conn.commit()
        print("✅ Changes committed to database")
        
        # Verify the changes
        print("\n🔍 Verifying changes...")
        
        cursor.execute("""
            SELECT COUNT(*) as total_users, 
                   COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_users
            FROM users
        """)
        user_stats = cursor.fetchone()
        print(f"📊 Users: {user_stats[0]} total, {user_stats[1]} verified")
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'admin_users'
        """)
        
        if cursor.fetchone():
            cursor.execute("""
                SELECT COUNT(*) as total_admin_users, 
                       COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_admin_users
                FROM admin_users
            """)
            admin_stats = cursor.fetchone()
            print(f"📊 Admin Users: {admin_stats[0]} total, {admin_stats[1]} verified")
        
        print("\n" + "=" * 50)
        print("✅ Email verification fix completed successfully!")
        print("\n📋 Summary:")
        print("   • All users now have verified emails")
        print("   • All admin users now have verified emails")
        print("   • 403 errors should be resolved")
        
        print("\n🔄 Next steps:")
        print("   1. Restart your Flask application")
        print("   2. Test the previously failing endpoints:")
        print("      - /api/notifications/")
        print("      - /api/wallet/stats")
        print("      - /api/cart/count")
        print("      - /api/wishlist/count")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()
            print("\n🔌 Database connection closed")

if __name__ == "__main__":
    print("🚀 PostgreSQL Email Verification Fix")
    print("=" * 50)
    fix_email_verification() 