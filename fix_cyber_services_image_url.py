#!/usr/bin/env python3
"""
Fix Cyber Services - Add missing image_url column
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService
from sqlalchemy import text

def fix_cyber_services_image_url():
    """Add image_url column to cyber_services table if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if image_url column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'cyber_services' 
                AND column_name = 'image_url'
            """))
            
            column_exists = result.fetchone() is not None
            
            if not column_exists:
                print("Adding image_url column to cyber_services table...")
                
                # Add the column
                db.session.execute(text("""
                    ALTER TABLE cyber_services 
                    ADD COLUMN image_url VARCHAR(500)
                """))
                
                db.session.commit()
                print("✅ image_url column added successfully!")
            else:
                print("✅ image_url column already exists!")
                
            # Verify the column was added
            result = db.session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'cyber_services' 
                AND column_name = 'image_url'
            """))
            
            column_info = result.fetchone()
            if column_info:
                print(f"✅ Column verified: {column_info[0]} ({column_info[1]})")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            return False
            
    return True

if __name__ == "__main__":
    print("🔧 Fixing Cyber Services image_url column...")
    success = fix_cyber_services_image_url()
    if success:
        print("✅ Cyber Services image_url fix completed successfully!")
    else:
        print("❌ Cyber Services image_url fix failed!") 