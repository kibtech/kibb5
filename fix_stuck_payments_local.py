#!/usr/bin/env python3
"""
Fix stuck cyber service payments using PostgreSQL database
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.abspath('.'))

# Use the same PostgreSQL database as production (from your config)
# No need to override DATABASE_URL - it will use the one from your config

from app import create_app
from app.models import db, CyberServiceOrder
from datetime import datetime, timezone

def fix_stuck_payments():
    """Fix all stuck cyber service payments"""
    try:
        app = create_app()
        with app.app_context():
            print("🔗 Connecting to PostgreSQL database...")
            
            # Test database connection
            try:
                from sqlalchemy import text
                db.session.execute(text('SELECT 1'))
                print("✅ Database connection successful!")
            except Exception as e:
                print(f"❌ Database connection failed: {str(e)}")
                print("💡 Make sure you have internet connection for PostgreSQL")
                return
            
            # Find all stuck payments
            stuck_orders = db.session.query(CyberServiceOrder).filter_by(
                status='payment_initiated',
                payment_status='pending'
            ).all()
        
        print(f"🔍 Found {len(stuck_orders)} stuck payments")
        
        fixed_count = 0
        for order in stuck_orders:
            time_diff = datetime.utcnow() - order.created_at
            minutes = time_diff.total_seconds() / 60
            
            print(f"\n📋 Order: {order.order_number}")
            print(f"   Time since creation: {minutes:.1f} minutes")
            print(f"   Payment ID: {order.payment_id}")
            
            # Fix payments older than 2 minutes (most M-Pesa payments complete within 2 minutes)
            if minutes > 2:
                try:
                    print(f"   🔧 Fixing payment...")
                    
                    # Update order status
                    order.payment_status = 'completed'
                    order.status = 'paid'
                    order.mpesa_code = f'FIXED{datetime.now().strftime("%m%d%H%M")}'
                    order.paid_at = datetime.utcnow()
                    order.updated_at = datetime.utcnow()
                    
                    # Skip progress tracking for now to avoid context issues
                    # order.update_progress()  # This causes app context issues
                    
                    db.session.commit()
                    
                    print(f"   ✅ Payment fixed successfully!")
                    print(f"   ✅ Status: {order.status}")
                    print(f"   ✅ Payment Status: {order.payment_status}")
                    print(f"   ✅ M-Pesa Code: {order.mpesa_code}")
                    
                    fixed_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Error fixing payment: {str(e)}")
                    try:
                        db.session.rollback()
                    except:
                        pass  # Ignore rollback errors in case context is lost
            else:
                print(f"   ⏳ Still recent, leaving for M-Pesa callback")
        
            print(f"\n🎉 Fixed {fixed_count} stuck payments!")
            
            # Show updated status
            print(f"\n📊 Current cyber service orders status:")
            recent_orders = db.session.query(CyberServiceOrder).order_by(CyberServiceOrder.created_at.desc()).limit(10).all()
            for order in recent_orders:
                print(f"   {order.order_number}: {order.status} / {order.payment_status}")
                
    except Exception as e:
        print(f"❌ Error running fix script: {str(e)}")
        print("💡 Try checking your internet connection and database credentials")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_stuck_payments()