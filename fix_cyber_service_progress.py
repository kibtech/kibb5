#!/usr/bin/env python3
"""
Fix Cyber Service Order Progress Stages
This script updates existing cyber service orders to have the correct progress stages
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_connection():
    """Get PostgreSQL database connection"""
    database_url = os.environ.get('DATABASE_URL') or 'postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres'
    
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def fix_cyber_service_progress():
    """Fix cyber service order progress stages"""
    print("🚀 Fixing cyber service order progress stages...")
    
    conn = get_database_connection()
    if not conn:
        print("❌ Could not connect to database.")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check current cyber service orders
        cursor.execute("SELECT id, status, payment_status, progress_stage FROM cyber_service_orders")
        orders = cursor.fetchall()
        
        print(f"📊 Found {len(orders)} cyber service orders to check")
        
        # Update cyber service orders with correct progress stages
        cursor.execute("""
            UPDATE cyber_service_orders 
            SET 
                progress_stage = CASE 
                    WHEN status = 'completed' THEN 'completed'
                    WHEN status = 'processing' THEN 'processing'
                    WHEN payment_status = 'completed' OR payment_status = 'paid' THEN 'payment_confirmed'
                    ELSE 'order_placed'
                END,
                progress_percentage = CASE 
                    WHEN status = 'completed' THEN 100
                    WHEN status = 'processing' THEN 70
                    WHEN payment_status = 'completed' OR payment_status = 'paid' THEN 30
                    ELSE 10
                END
        """)
        
        updated_rows = cursor.rowcount
        print(f"✅ Updated {updated_rows} cyber service orders with correct progress stages")
        
        # Show the updated orders
        cursor.execute("""
            SELECT id, order_number, status, payment_status, progress_stage, progress_percentage 
            FROM cyber_service_orders 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        
        updated_orders = cursor.fetchall()
        print("\n📋 Updated orders preview:")
        for order in updated_orders:
            print(f"  Order {order[1]}: {order[2]} | {order[3]} | {order[4]} ({order[5]}%)")
        
        # Commit the changes
        conn.commit()
        print("\n✅ Cyber service progress fix completed successfully!")
        
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Fix failed: {e}")
        return False
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Fix Cyber Service Order Progress Stages")
    print("=" * 60)
    
    success = fix_cyber_service_progress()
    
    if success:
        print("\n🎉 Fix completed successfully!")
        print("🔄 Refresh your orders page to see the correct progress stages.")
    else:
        print("\n❌ Fix failed! Please check the errors above.")
        sys.exit(1)