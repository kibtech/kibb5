#!/usr/bin/env python3
"""
Migration script to add wallet_pin column to users table
"""

from app import create_app, db
from app.models import User
from sqlalchemy import text

def migrate_wallet_pin():
    """Add wallet_pin column to users table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add wallet_pin column if it doesn't exist
            with db.engine.connect() as conn:
                # Check if column exists
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    AND column_name = 'wallet_pin'
                """))
                
                if not result.fetchone():
                    print("Adding wallet_pin column to users table...")
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN wallet_pin VARCHAR(128)
                    """))
                    conn.commit()
                    print("✅ wallet_pin column added successfully!")
                else:
                    print("✅ wallet_pin column already exists!")
            
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            raise

if __name__ == "__main__":
    migrate_wallet_pin() 