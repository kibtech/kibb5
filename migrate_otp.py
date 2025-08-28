#!/usr/bin/env python3
"""
Migration script to add OTP functionality to KibTech database
Adds OTP table and email_verified field to User model
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, OTP
from sqlalchemy import text

def migrate_otp():
    """Add OTP table and email_verified field"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Starting OTP migration...")
        
        try:
            # Check if email_verified column exists in users table
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'email_verified'
            """))
            
            if not result.fetchone():
                print("📝 Adding email_verified column to users table...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN email_verified BOOLEAN DEFAULT FALSE
                """))
                print("✅ Added email_verified column")
            else:
                print("ℹ️  email_verified column already exists")
            
            # Check if otps table exists
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'otps'
            """))
            
            if not result.fetchone():
                print("📝 Creating otps table...")
                db.session.execute(text("""
                    CREATE TABLE otps (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id),
                        email VARCHAR(120) NOT NULL,
                        otp_code VARCHAR(6) NOT NULL,
                        purpose VARCHAR(50) NOT NULL,
                        is_used BOOLEAN DEFAULT FALSE,
                        expires_at TIMESTAMP NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                print("✅ Created otps table")
            else:
                print("ℹ️  otps table already exists")
            
            # Create indexes for better performance
            print("📝 Creating indexes...")
            
            # Index for OTP lookups
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_otps_email_purpose 
                ON otps(email, purpose)
            """))
            
            # Index for expired OTP cleanup
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_otps_expires_at 
                ON otps(expires_at)
            """))
            
            # Index for user OTPs
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_otps_user_id 
                ON otps(user_id)
            """))
            
            print("✅ Created indexes")
            
            db.session.commit()
            
            print("\n🎉 OTP migration completed successfully!")
            print("\n📋 What was added:")
            print("   - email_verified column to users table")
            print("   - otps table with all required fields")
            print("   - Performance indexes for OTP operations")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Migration failed: {str(e)}")
            return False
        
        return True

if __name__ == '__main__':
    migrate_otp() 