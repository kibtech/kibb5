#!/usr/bin/env python3
"""
Direct database fix using environment variables
"""

import os
import psycopg2

def fix_database():
    """Add missing email_verified column to users table"""
    print("🔧 Direct Database Fix")
    print("=" * 30)
    
    try:
        # Get database connection details from environment
        db_host = os.getenv('DB_HOST', 'localhost')
        db_name = os.getenv('DB_NAME', 'kibtech')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'password')
        db_port = os.getenv('DB_PORT', '5432')
        
        print(f"Connecting to database: {db_host}:{db_port}/{db_name}")
        
        # Connect to database
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
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
            print("Adding email_verified column...")
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
    print("Starting direct database fix...")
    fix_database()
    print("Script completed.") 