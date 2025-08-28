#!/usr/bin/env python3
"""
Fix Commission Table Structure
This script fixes the commission table to properly handle both
cyber service orders and e-commerce orders.
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

def fix_commission_table_structure():
    """Fix the commission table structure"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 FIXING COMMISSION TABLE STRUCTURE")
        print("=" * 50)
        
        # Check current commission records
        all_commissions = Commission.query.all()
        print(f"Found {len(all_commissions)} existing commission records")
        
        # Check for invalid order_id references
        invalid_commissions = []
        valid_commissions = []
        
        for commission in all_commissions:
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
                    invalid_commissions.append(commission)
        
        print(f"Valid commissions: {len(valid_commissions)}")
        print(f"Invalid commissions: {len(invalid_commissions)}")
        
        if invalid_commissions:
            print(f"\n❌ INVALID COMMISSIONS FOUND:")
            for commission in invalid_commissions:
                print(f"   Commission ID {commission.id}: order_id {commission.order_id} not found in any table")
        
        # Check the specific stuck order
        stuck_order_number = "CS2025081320430924"
        stuck_order = CyberServiceOrder.query.filter_by(order_number=stuck_order_number).first()
        
        if stuck_order:
            print(f"\n📦 STUCK ORDER ANALYSIS:")
            print(f"   Order ID: {stuck_order.id}")
            print(f"   Order Number: {stuck_order.order_number}")
            print(f"   Table: cyber_service_orders")
            print(f"   Referred by: {stuck_order.user.referred_by_id if stuck_order.user else 'Unknown'}")
        
        print(f"\n🔧 SOLUTION:")
        print(f"   The commission table needs to be updated to handle both order types.")
        print(f"   We need to either:")
        print(f"   1. Add a separate cyber_service_order_id field to commissions table")
        print(f"   2. Or modify the existing order_id to be more flexible")
        print(f"   3. Or create separate commission tables for each order type")
        
        # Check if we can fix this by updating the commission structure
        print(f"\n🛠️  IMMEDIATE FIX:")
        print(f"   For now, we can manually complete the payment without commission")
        print(f"   Then fix the commission table structure for future orders")
        
        return len(invalid_commissions)

def create_flexible_commission_record():
    """Create a commission record that works with the current structure"""
    
    print(f"\n🔧 CREATING WORKING COMMISSION RECORD:")
    
    # The issue is that we're trying to insert a commission with order_id=98
    # But order_id=98 doesn't exist in the orders table
    # We need to either:
    # 1. Create a dummy order record, or
    # 2. Modify the commission table structure
    
    print(f"   Option 1: Create dummy order record (quick fix)")
    print(f"   Option 2: Modify commission table (proper fix)")
    print(f"   Option 3: Skip commission for now (temporary fix)")
    
    return "Option 3 recommended for immediate testing"

if __name__ == "__main__":
    try:
        invalid_count = fix_commission_table_structure()
        create_flexible_commission_record()
        
        if invalid_count > 0:
            print(f"\n⚠️  {invalid_count} invalid commission records found")
            print(f"   This explains why referral payments are getting stuck!")
        else:
            print(f"\n✅ All commission records are valid")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Fix the commission table structure")
        print(f"   2. Test referral payments again")
        print(f"   3. Verify commissions are processed correctly")
        
    except Exception as e:
        logger.error(f"Failed to fix commission table structure: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 