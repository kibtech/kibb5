#!/usr/bin/env python3
"""
Simple SQL fix for missing email_verified column
"""

import psycopg2

def fix_database():
    """Add missing email_verified column"""
    print("🔧 Simple Database Fix")
    print("=" * 30)
    
    # Railway database connection
    DATABASE_URL = "postgresql://postgres:UyAUrqMDtsFssWrwYdYRaqNfNMFpNbqW@trolley.proxy.rlwy.net:20673/railway"
    
    try:
        print("Connecting to Railway database...")
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Connected successfully")
        
        cur = conn.cursor()
        
        # Add the column
        print("Adding email_verified column...")
        cur.execute("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE")
        conn.commit()
        print("✅ Column added successfully")
        
        # Verify
        cur.execute("SELECT email_verified FROM users LIMIT 1")
        print("✅ Column verification successful")
        
        cur.close()
        conn.close()
        print("🎉 Database fixed!")
        
    except psycopg2.errors.DuplicateColumn:
        print("✅ Column already exists")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Starting fix...")
    fix_database()
    print("Done.") 