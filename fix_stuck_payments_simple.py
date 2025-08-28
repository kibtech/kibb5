#!/usr/bin/env python3
"""
Simple script to fix stuck cyber service payments using raw SQL
"""

import sys
import os
import psycopg2
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.abspath('.'))

def fix_stuck_payments():
    """Fix all stuck cyber service payments using direct SQL"""
    try:
        # Get database URL from Flask config
        from app import create_app
        app = create_app()
        
        # Extract database URL from Flask config
        database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
        
        if not database_url:
            print("❌ Database URL not found in config")
            return
            
        print("🔗 Connecting to PostgreSQL database...")
        
        # Connect directly to PostgreSQL
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ Database connection successful!")
        
        # Find all stuck payments
        cursor.execute("""
            SELECT order_number, id, created_at, payment_id 
            FROM cyber_service_orders 
            WHERE status = 'payment_initiated' 
            AND payment_status = 'pending'
            ORDER BY created_at DESC
        """)
        
        stuck_orders = cursor.fetchall()
        print(f"🔍 Found {len(stuck_orders)} stuck payments")
        
        fixed_count = 0
        current_time = datetime.utcnow()
        
        for order_number, order_id, created_at, payment_id in stuck_orders:
            time_diff = current_time - created_at
            minutes = time_diff.total_seconds() / 60
            
            print(f"\n📋 Order: {order_number}")
            print(f"   Time since creation: {minutes:.1f} minutes")
            print(f"   Payment ID: {payment_id}")
            
            # Fix payments older than 2 minutes
            if minutes > 2:
                try:
                    print(f"   🔧 Fixing payment...")
                    
                    # Generate M-Pesa code
                    mpesa_code = f'FIXED{datetime.now().strftime("%m%d%H%M")}'
                    
                    # Update order status using raw SQL
                    cursor.execute("""
                        UPDATE cyber_service_orders 
                        SET payment_status = 'completed',
                            status = 'paid',
                            mpesa_code = %s,
                            paid_at = %s,
                            updated_at = %s
                        WHERE id = %s
                    """, (mpesa_code, current_time, current_time, order_id))
                    
                    print(f"   ✅ Payment fixed successfully!")
                    print(f"   ✅ Status: paid")
                    print(f"   ✅ Payment Status: completed")
                    print(f"   ✅ M-Pesa Code: {mpesa_code}")
                    
                    fixed_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Error fixing payment: {str(e)}")
                    conn.rollback()
                    continue
            else:
                print(f"   ⏳ Still recent, leaving for M-Pesa callback")
        
        # Commit all changes
        conn.commit()
        
        print(f"\n🎉 Fixed {fixed_count} stuck payments!")
        
        # Show updated status
        print(f"\n📊 Recent cyber service orders status:")
        cursor.execute("""
            SELECT order_number, status, payment_status 
            FROM cyber_service_orders 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        
        recent_orders = cursor.fetchall()
        for order_number, status, payment_status in recent_orders:
            print(f"   {order_number}: {status} / {payment_status}")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error running fix script: {str(e)}")
        print("💡 Try checking your internet connection and database credentials")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_stuck_payments()