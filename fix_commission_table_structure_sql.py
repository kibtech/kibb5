#!/usr/bin/env python3
"""
Fix Commission Table Structure - SQL Commands
This script generates the SQL commands needed to fix the commission table structure.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import Commission
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_fix_sql_commands():
    """Generate SQL commands to fix the commission table structure"""
    
    print("🔧 GENERATING SQL FIX COMMANDS")
    print("=" * 50)
    
    print("📝 SQL COMMANDS TO FIX COMMISSION TABLE:")
    print("-" * 50)
    
    # SQL commands to fix the table structure
    sql_commands = [
        "-- Step 1: Add cyber_service_order_id field",
        "ALTER TABLE commissions ADD COLUMN cyber_service_order_id INTEGER;",
        "",
        "-- Step 2: Make order_id nullable (since cyber services won't use it)",
        "ALTER TABLE commissions ALTER COLUMN order_id DROP NOT NULL;",
        "",
        "-- Step 3: Add foreign key constraint for cyber service orders",
        "ALTER TABLE commissions ADD CONSTRAINT fk_cyber_service_order",
        "    FOREIGN KEY (cyber_service_order_id) REFERENCES cyber_service_orders(id);",
        "",
        "-- Step 4: Add index for better performance",
        "CREATE INDEX idx_commissions_cyber_service_order_id ON commissions(cyber_service_order_id);",
        "",
        "-- Step 5: Verify the changes",
        "\\d commissions;",
        ""
    ]
    
    for command in sql_commands:
        print(command)
    
    print("📋 MANUAL EXECUTION STEPS:")
    print("-" * 50)
    print("1. Connect to your PostgreSQL database")
    print("2. Run each ALTER TABLE command above")
    print("3. Verify the table structure with \\d commissions")
    print("4. Test with a small referral payment")
    
    print("\n⚠️  IMPORTANT SAFETY NOTES:")
    print("-" * 50)
    print("• Backup your database before making changes")
    print("• Test in development environment first")
    print("• Run commands during low-traffic periods")
    print("• Verify each command completes successfully")
    
    return sql_commands

def check_current_table_structure():
    """Check the current commission table structure"""
    
    app = create_app()
    
    with app.app_context():
        print("\n🔍 CURRENT COMMISSION TABLE STRUCTURE:")
        print("=" * 50)
        
        try:
            # Get table info using raw SQL
            result = db.session.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'commissions'
                ORDER BY ordinal_position;
            """)
            
            columns = result.fetchall()
            
            if columns:
                print("   Current columns:")
                for col in columns:
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    default = f" DEFAULT {col[3]}" if col[3] else ""
                    print(f"      {col[0]}: {col[1]} {nullable}{default}")
            else:
                print("   No columns found (table might not exist)")
                
        except Exception as e:
            print(f"   Error checking table structure: {str(e)}")
        
        # Check foreign key constraints
        try:
            result = db.session.execute("""
                SELECT 
                    tc.constraint_name, 
                    tc.table_name, 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                  AND tc.table_name='commissions';
            """)
            
            constraints = result.fetchall()
            
            if constraints:
                print("\n   Foreign key constraints:")
                for constraint in constraints:
                    print(f"      {constraint[2]} -> {constraint[3]}.{constraint[4]}")
            else:
                print("\n   No foreign key constraints found")
                
        except Exception as e:
            print(f"   Error checking constraints: {str(e)}")

def create_test_commission_record():
    """Create a test commission record to verify the fix"""
    
    print("\n🧪 TEST COMMISSION RECORD CREATION:")
    print("=" * 50)
    
    print("   After running the SQL fixes, you can test with:")
    print("   1. Make a small referral payment (KSh 1)")
    print("   2. Check if commission is created successfully")
    print("   3. Verify the commission record has correct references")
    
    print("\n   Expected result:")
    print("   ✅ Payment completes successfully")
    print("   ✅ Commission record created")
    print("   ✅ Referrer wallet updated")
    print("   ✅ No database constraint errors")

if __name__ == "__main__":
    try:
        generate_fix_sql_commands()
        check_current_table_structure()
        create_test_commission_record()
        
        print("\n🎯 EXECUTION PLAN:")
        print("=" * 50)
        print("1. ✅ Cleaned up broken commission records")
        print("2. 🔧 Run SQL commands to fix table structure")
        print("3. 🧪 Test with a small referral payment")
        print("4. 💰 Verify commission processing works")
        
        print("\n💡 READY TO FIX:")
        print("   Copy the SQL commands above and run them in your database")
        print("   This will fix the commission table structure permanently!")
        
    except Exception as e:
        logger.error(f"Failed to generate SQL commands: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 