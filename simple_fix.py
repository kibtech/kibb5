#!/usr/bin/env python3
"""
Simple database fix script
"""

import psycopg2
from config import Config

def fix_database():
    """Add missing email_verified column to users table"""
    print("🔧 Simple Database Fix")
    print("=" * 30)
    
    try:
        # Connect to database
        print("Connecting to database...")
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        print("✅ Database connected successfully")
        
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
            cur.execute("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE")
            conn.commit()
            print("✅ email_verified column added successfully")
            
            # Verify the column was added
            cur.execute("SELECT email_verified FROM users LIMIT 1")
            print("✅ Column verification successful")
            
            print("\n🎉 Database schema fixed successfully!")
            
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
    print("Starting simple database fix...")
    fix_database()
    print("Script completed.") 