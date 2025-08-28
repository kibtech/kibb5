#!/usr/bin/env python3
"""
Fix Railway database by adding missing email_verified column
"""

import psycopg2
import os

def fix_railway_database():
    """Add missing email_verified column to Railway database"""
    print("🔧 Fixing Railway Database")
    print("=" * 40)
    
    # Railway database connection details
    db_url = "postgresql://postgres:UyAUrqMDtsFssWrwYdYRaqNfNMFpNbqW@trolley.proxy.rlwy.net:20673/railway"
    
    try:
        print("Connecting to Railway database...")
        conn = psycopg2.connect(db_url)
        print("✅ Connected to Railway database successfully")
        
        # Create cursor
        cur = conn.cursor()
        
        # Check if column exists
        try:
            print("Checking if email_verified column exists...")
            cur.execute("SELECT email_verified FROM users LIMIT 1")
            print("✅ email_verified column already exists")
            return
        except psycopg2.errors.UndefinedColumn:
            print("❌ email_verified column is missing - adding it now...")
        
        # Add the column
        try:
            print("Adding email_verified column to users table...")
            cur.execute("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE")
            conn.commit()
            print("✅ email_verified column added successfully")
            
            # Verify the column was added
            cur.execute("SELECT email_verified FROM users LIMIT 1")
            print("✅ Column verification successful")
            
            print("\n🎉 Railway database schema fixed successfully!")
            
        except Exception as e:
            print(f"❌ Error adding column: {str(e)}")
            conn.rollback()
            raise
        
        finally:
            cur.close()
            conn.close()
            
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting Railway database fix...")
    fix_railway_database()
    print("Script completed.") 