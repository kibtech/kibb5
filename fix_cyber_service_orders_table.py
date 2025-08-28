#!/usr/bin/env python3
"""
Fix CyberServiceOrder table by adding missing updated_at column
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberServiceOrder
from datetime import datetime
from sqlalchemy import text

def fix_cyber_service_orders_table():
    """Add updated_at column to cyber_service_orders table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add the updated_at column
            with db.engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE cyber_service_orders 
                    ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                """))
                conn.commit()
            
            # Update existing records to have updated_at = created_at
            with db.engine.connect() as conn:
                conn.execute(text("""
                    UPDATE cyber_service_orders 
                    SET updated_at = created_at 
                    WHERE updated_at IS NULL
                """))
                conn.commit()
            
            print("✅ Successfully added updated_at column to cyber_service_orders table")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            # Check if column already exists
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'cyber_service_orders' 
                        AND column_name = 'updated_at'
                    """))
                    if result.fetchone():
                        print("✅ updated_at column already exists")
                    else:
                        print("❌ Column does not exist and could not be created")
            except Exception as check_error:
                print(f"❌ Could not check column existence: {check_error}")

if __name__ == "__main__":
    fix_cyber_service_orders_table() 