#!/usr/bin/env python3
"""
Migration script to add PIN security fields to users table
"""
from app import create_app, db
from app.models import User
from sqlalchemy import text

def migrate_pin_security():
    app = create_app()
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Check if pin_attempts column exists
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    AND column_name = 'pin_attempts'
                """))
                
                if not result.fetchone():
                    print("Adding PIN security columns to users table...")
                    
                    # Add pin_attempts column
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN pin_attempts INTEGER DEFAULT 0
                    """))
                    
                    # Add pin_locked_until column
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN pin_locked_until TIMESTAMP
                    """))
                    
                    # Add last_pin_attempt column
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN last_pin_attempt TIMESTAMP
                    """))
                    
                    conn.commit()
                    print("✅ PIN security columns added successfully!")
                else:
                    print("✅ PIN security columns already exist!")
                    
            print("Migration completed successfully!")
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            raise

if __name__ == "__main__":
    migrate_pin_security() 