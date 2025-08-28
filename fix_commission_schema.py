#!/usr/bin/env python3
"""
Database migration script to update commissions table for manual commissions
"""

from app import create_app, db
from app.models import Commission
from sqlalchemy import text

def migrate_commission_schema():
    """Update commissions table schema to support manual commissions"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if the new columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('commissions')]
            
            print("Current commission table columns:", columns)
            
            # Add new columns if they don't exist
            if 'commission_type' not in columns:
                print("Adding commission_type column...")
                db.session.execute(text("""
                    ALTER TABLE commissions 
                    ADD COLUMN commission_type VARCHAR(20) DEFAULT 'order'
                """))
                print("✓ commission_type column added")
            
            if 'description' not in columns:
                print("Adding description column...")
                db.session.execute(text("""
                    ALTER TABLE commissions 
                    ADD COLUMN description TEXT
                """))
                print("✓ description column added")
            
            # Make order_id nullable if it's not already
            # First check if order_id is nullable
            order_id_info = next((col for col in inspector.get_columns('commissions') if col['name'] == 'order_id'), None)
            if order_id_info and order_id_info['nullable'] == False:
                print("Making order_id nullable...")
                db.session.execute(text("""
                    ALTER TABLE commissions 
                    ALTER COLUMN order_id DROP NOT NULL
                """))
                print("✓ order_id made nullable")
            
            db.session.commit()
            print("✓ Database migration completed successfully!")
            
            # Update existing commission records to have proper type
            existing_commissions = Commission.query.all()
            updated_count = 0
            
            for commission in existing_commissions:
                if not hasattr(commission, 'commission_type') or commission.commission_type is None:
                    commission.commission_type = 'order'
                    updated_count += 1
            
            if updated_count > 0:
                db.session.commit()
                print(f"✓ Updated {updated_count} existing commission records")
            
            print("Migration completed successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error during migration: {str(e)}")
            raise

if __name__ == "__main__":
    migrate_commission_schema() 