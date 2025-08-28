#!/usr/bin/env python3
"""
Fix payment_id column type in cyber_service_orders table
"""

from app import create_app, db
from sqlalchemy import text

def fix_payment_id_column():
    """Change payment_id column from INTEGER to STRING"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Fixing payment_id column type...")
            
            # Check if column exists and its current type
            with db.engine.connect() as conn:
                # Check current column type
                result = conn.execute(text("""
                    SELECT data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'cyber_service_orders' 
                    AND column_name = 'payment_id'
                """))
                column_info = result.fetchone()
                
                if not column_info:
                    print("❌ payment_id column not found!")
                    return False
                
                current_type = column_info[0]
                print(f"📊 Current payment_id type: {current_type}")
                
                if current_type == 'character varying':
                    print("✅ payment_id column is already STRING type")
                    return True
                
                # Change column type from INTEGER to STRING
                print("🔄 Changing payment_id from INTEGER to STRING...")
                
                # First, drop the foreign key constraint if it exists
                try:
                    conn.execute(text("""
                        ALTER TABLE cyber_service_orders 
                        DROP CONSTRAINT IF EXISTS cyber_service_orders_payment_id_fkey
                    """))
                    print("✅ Dropped foreign key constraint")
                except Exception as e:
                    print(f"ℹ️ No foreign key constraint to drop: {e}")
                
                # Change column type
                conn.execute(text("""
                    ALTER TABLE cyber_service_orders 
                    ALTER COLUMN payment_id TYPE VARCHAR(50)
                """))
                
                conn.commit()
                print("✅ Successfully changed payment_id to VARCHAR(50)")
                
                # Verify the change
                result = conn.execute(text("""
                    SELECT data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'cyber_service_orders' 
                    AND column_name = 'payment_id'
                """))
                new_type = result.fetchone()[0]
                print(f"✅ Verified new type: {new_type}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error fixing payment_id column: {e}")
            return False

if __name__ == "__main__":
    success = fix_payment_id_column()
    if success:
        print("🎉 Payment ID column fix completed successfully!")
    else:
        print("💥 Payment ID column fix failed!") 