#!/usr/bin/env python3
"""
Script to run the email verification database migration
This will update all existing users to have verified emails
"""

import os
import psycopg2
from urllib.parse import urlparse

def get_database_connection():
    """Get database connection from environment variables"""
    try:
        # Try to get DATABASE_URL from environment
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Parse the DATABASE_URL
            parsed = urlparse(database_url)
            
            # Extract connection parameters
            host = parsed.hostname
            port = parsed.port or 5432
            database = parsed.path[1:]  # Remove leading slash
            username = parsed.username
            password = parsed.password
            
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password
            )
            print(f"✅ Connected to PostgreSQL database: {database}")
            return conn
        else:
            print("❌ DATABASE_URL environment variable not found")
            print("Please set your DATABASE_URL environment variable")
            return None
            
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def run_migration(conn):
    """Run the email verification migration"""
    try:
        cursor = conn.cursor()
        
        print("\n🚀 Starting email verification migration...")
        
        # Step 1: Update users table
        print("📝 Updating users table...")
        cursor.execute("UPDATE users SET email_verified = TRUE")
        users_updated = cursor.rowcount
        print(f"✅ Updated {users_updated} users")
        
        # Step 2: Update admin_users table
        print("📝 Updating admin_users table...")
        cursor.execute("UPDATE admin_users SET email_verified = TRUE")
        admin_users_updated = cursor.rowcount
        print(f"✅ Updated {admin_users_updated} admin users")
        
        # Commit the changes
        conn.commit()
        print("✅ Changes committed to database")
        
        # Step 3: Verify the changes
        print("\n🔍 Verifying changes...")
        
        # Check users table
        cursor.execute("""
            SELECT COUNT(*) as total_users, 
                   COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_users
            FROM users
        """)
        user_stats = cursor.fetchone()
        print(f"📊 Users: {user_stats[0]} total, {user_stats[1]} verified")
        
        # Check admin_users table
        cursor.execute("""
            SELECT COUNT(*) as total_admin_users, 
                   COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_admin_users
            FROM admin_users
        """)
        admin_stats = cursor.fetchone()
        print(f"📊 Admin Users: {admin_stats[0]} total, {admin_stats[1]} verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        conn.rollback()
        return False

def main():
    """Main function to run the migration"""
    print("🚀 Email Verification Database Migration")
    print("=" * 50)
    
    # Connect to database
    conn = get_database_connection()
    if not conn:
        print("\n❌ Migration failed - could not connect to database")
        return
    
    try:
        # Run the migration
        success = run_migration(conn)
        
        if success:
            print("\n" + "=" * 50)
            print("✅ Migration completed successfully!")
            print("\n📋 Summary:")
            print("   • All users now have verified emails")
            print("   • All admin users now have verified emails")
            print("   • Email verification is no longer required")
            
            print("\n🔄 Next steps:")
            print("   1. Restart your Flask application")
            print("   2. Test user registration (should work without email verification)")
            print("   3. Test password reset (should work without email verification)")
            print("   4. Test user login (should work without email verification)")
        else:
            print("\n❌ Migration failed")
            
    finally:
        conn.close()
        print("\n🔌 Database connection closed")

if __name__ == "__main__":
    main() 