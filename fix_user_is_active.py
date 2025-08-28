#!/usr/bin/env python3
"""
Script to add is_active column to users table and set all existing users as active
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from sqlalchemy import text

def fix_user_is_active():
    """Add is_active column to users table and set all users as active"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if is_active column already exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'is_active'
            """)).fetchone()
            
            if result:
                print("is_active column already exists in users table")
                return
            
            # Add is_active column
            print("Adding is_active column to users table...")
            db.session.execute(text("""
                ALTER TABLE users 
                ADD COLUMN is_active BOOLEAN DEFAULT TRUE
            """))
            
            # Update all existing users to be active
            print("Setting all existing users as active...")
            db.session.execute(text("""
                UPDATE users 
                SET is_active = TRUE 
                WHERE is_active IS NULL
            """))
            
            db.session.commit()
            print("Successfully added is_active column and updated existing users")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            raise

if __name__ == "__main__":
    fix_user_is_active() 