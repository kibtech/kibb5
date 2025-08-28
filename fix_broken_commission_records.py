#!/usr/bin/env python3
"""
Fix Broken Commission Records
This script cleans up broken commission records and fixes the table structure.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import Commission, CyberServiceOrder, Order
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_broken_commission_records():
    """Fix broken commission records"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 FIXING BROKEN COMMISSION RECORDS")
        print("=" * 50)
        
        # Check current commission records
        all_commissions = Commission.query.all()
        print(f"Found {len(all_commissions)} existing commission records")
        
        # Find broken records
        broken_commissions = []
        valid_commissions = []
        
        for commission in all_commissions:
            if commission.order_id is None:
                broken_commissions.append(commission)
            else:
                # Check if order_id exists in orders table
                order = Order.query.get(commission.order_id)
                if order:
                    valid_commissions.append(commission)
                else:
                    # Check if it's a cyber service order
                    cyber_order = CyberServiceOrder.query.get(commission.order_id)
                    if cyber_order:
                        valid_commissions.append(commission)
                    else:
                        broken_commissions.append(commission)
        
        print(f"Valid commissions: {len(valid_commissions)}")
        print(f"Broken commissions: {len(broken_commissions)}")
        
        if broken_commissions:
            print(f"\n❌ BROKEN COMMISSIONS FOUND:")
            for commission in broken_commissions:
                print(f"   Commission ID {commission.id}: order_id = {commission.order_id}")
                print(f"      Amount: {commission.amount}")
                print(f"      Referrer ID: {commission.referrer_id}")
                print(f"      Type: {commission.commission_type}")
                print(f"      Created: {commission.created_at}")
                print()
        
        # Ask for confirmation before deletion
        if broken_commissions:
            print(f"⚠️  WARNING: {len(broken_commissions)} broken commission records found!")
            print(f"   These records have invalid order_id references and cannot be used.")
            print(f"   Recommendation: Delete them and start fresh.")
            
            # Delete broken records
            print(f"\n🗑️  DELETING BROKEN COMMISSION RECORDS...")
            for commission in broken_commissions:
                db.session.delete(commission)
                print(f"   Deleted Commission ID {commission.id}")
            
            # Commit the deletions
            db.session.commit()
            print(f"   ✅ Deleted {len(broken_commissions)} broken commission records")
        else:
            print(f"\n✅ No broken commission records found!")
        
        # Check remaining valid records
        remaining_commissions = Commission.query.all()
        print(f"\n📊 REMAINING COMMISSION RECORDS: {len(remaining_commissions)}")
        
        if remaining_commissions:
            print(f"   Valid commission records remaining:")
            for commission in remaining_commissions:
                print(f"      ID {commission.id}: order_id {commission.order_id}, amount {commission.amount}")
        
        return len(broken_commissions)

def analyze_commission_table_structure():
    """Analyze the current commission table structure"""
    
    print(f"\n🔍 COMMISSION TABLE STRUCTURE ANALYSIS:")
    print(f"=" * 50)
    
    # Check what fields exist in the commission table
    print(f"   Current commission table fields:")
    print(f"      - id (Primary Key)")
    print(f"      - referrer_id (Foreign Key to users)")
    print(f"      - order_id (Foreign Key to orders)")
    print(f"      - amount")
    print(f"      - commission_type")
    print(f"      - description")
    print(f"      - created_at")
    
    print(f"\n🔧 PROBLEM IDENTIFIED:")
    print(f"   The commission table has 'order_id' which only references 'orders' table")
    print(f"   But cyber service orders are in 'cyber_service_orders' table")
    print(f"   This creates a foreign key constraint violation")
    
    print(f"\n💡 SOLUTION OPTIONS:")
    print(f"   1. Add 'cyber_service_order_id' field to commissions table")
    print(f"   2. Modify 'order_id' to be nullable and handle both types")
    print(f"   3. Create separate commission tables for each order type")
    
    print(f"\n🎯 RECOMMENDED SOLUTION:")
    print(f"   Option 1: Add 'cyber_service_order_id' field")
    print(f"   This maintains data integrity and allows both order types")

def create_fixed_commission_structure():
    """Create a fixed commission structure"""
    
    print(f"\n🔧 CREATING FIXED COMMISSION STRUCTURE:")
    print(f"=" * 50)
    
    print(f"   To fix this properly, you need to:")
    print(f"   1. Add a new field 'cyber_service_order_id' to commissions table")
    print(f"   2. Make 'order_id' nullable (since cyber services won't use it)")
    print(f"   3. Update the commission creation logic to use the correct field")
    
    print(f"\n📝 SQL ALTER TABLE COMMANDS NEEDED:")
    print(f"   ALTER TABLE commissions ADD COLUMN cyber_service_order_id INTEGER;")
    print(f"   ALTER TABLE commissions ALTER COLUMN order_id DROP NOT NULL;")
    print(f"   ALTER TABLE commissions ADD CONSTRAINT fk_cyber_service_order")
    print(f"      FOREIGN KEY (cyber_service_order_id) REFERENCES cyber_service_orders(id);")
    
    print(f"\n⚠️  IMPORTANT:")
    print(f"   This requires database schema changes")
    print(f"   Test in development environment first")
    print(f"   Backup your database before making changes")

if __name__ == "__main__":
    try:
        deleted_count = fix_broken_commission_records()
        analyze_commission_table_structure()
        create_fixed_commission_structure()
        
        if deleted_count > 0:
            print(f"\n🎉 SUCCESS: Deleted {deleted_count} broken commission records!")
            print(f"   Your commission table is now clean")
            print(f"   Next step: Fix the table structure for future commissions")
        else:
            print(f"\n✅ No broken records to fix")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. ✅ Cleaned up broken commission records")
        print(f"   2. 🔧 Fix commission table structure (add cyber_service_order_id)")
        print(f"   3. 🧪 Test referral payments")
        print(f"   4. 💰 Verify commissions are processed correctly")
        
    except Exception as e:
        logger.error(f"Failed to fix broken commission records: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 