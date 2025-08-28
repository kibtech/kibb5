#!/usr/bin/env python3
"""
Simple script to run the email verification database migration
Connects directly to your Supabase PostgreSQL database
"""

import psycopg2

def run_migration():
    """Run the email verification migration"""
    # Your Supabase database connection details from config.py
    # Try the working hostname first
    database_url = "postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres"
    
    # Alternative connection string if the first one fails
    alternative_url = "postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@fcrvabkgdhdvprwwlyuf.supabase.co:5432/postgres"
    
    try:
        print("🚀 Connecting to Supabase database...")
        
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
    print("🚀 Email Verification Database Migration")
    print("=" * 50)
    run_migration() 