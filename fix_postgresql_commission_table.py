#!/usr/bin/env python3
"""
Fix PostgreSQL Commission Table Structure
This script directly connects to your PostgreSQL database and fixes the commission table.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from config import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_database_connection():
    """Get direct database connection"""
    
    # Get database URI from config
    app = create_app()
    with app.app_context():
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    
    print(f"🔗 Connecting to database...")
    print(f"   URI: {db_uri.split('@')[1] if '@' in db_uri else 'Local database'}")
    
    try:
        # Parse connection string
        if 'postgresql://' in db_uri:
            # Extract connection details
            uri_parts = db_uri.replace('postgresql://', '').split('@')
            if len(uri_parts) == 2:
                auth_part = uri_parts[0]
                host_part = uri_parts[1]
                
                username, password = auth_part.split(':')
                host_port, database = host_part.split('/')
                host, port = host_port.split(':') if ':' in host_port else (host_port, '5432')
                
                # Connect to database
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=username,
                    password=password
                )
                
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                print(f"   ✅ Connected successfully!")
                return conn
            else:
                raise Exception("Invalid database URI format")
        else:
            raise Exception("Not a PostgreSQL database")
            
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        return None

def check_current_table_structure(conn):
    """Check current commission table structure"""
    
    print(f"\n🔍 CHECKING CURRENT TABLE STRUCTURE:")
    print("=" * 50)
    
    try:
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'commissions'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("   ❌ Commissions table does not exist!")
            return False
        
        print("   ✅ Commissions table exists")
        
        # Get current columns
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'commissions'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print(f"\n   Current columns:")
        for col in columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            default = f" DEFAULT {col[3]}" if col[3] else ""
            print(f"      {col[0]}: {col[1]} {nullable}{default}")
        
        # Check foreign key constraints
        cursor.execute("""
            SELECT 
                tc.constraint_name, 
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
        
        constraints = cursor.fetchall()
        
        if constraints:
            print(f"\n   Foreign key constraints:")
            for constraint in constraints:
                print(f"      {constraint[1]} -> {constraint[2]}.{constraint[3]}")
        else:
            print(f"\n   No foreign key constraints found")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking structure: {str(e)}")
        return False

def fix_commission_table_structure(conn):
    """Fix the commission table structure"""
    
    print(f"\n🔧 FIXING COMMISSION TABLE STRUCTURE:")
    print("=" * 50)
    
    try:
        cursor = conn.cursor()
        
        # Step 1: Add cyber_service_order_id field
        print("   Step 1: Adding cyber_service_order_id field...")
        try:
            cursor.execute("""
                ALTER TABLE commissions 
                ADD COLUMN cyber_service_order_id INTEGER;
            """)
            print("      ✅ cyber_service_order_id field added")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("      ℹ️  cyber_service_order_id field already exists")
            else:
                print(f"      ❌ Error: {str(e)}")
                return False
        
        # Step 2: Make order_id nullable
        print("   Step 2: Making order_id nullable...")
        try:
            cursor.execute("""
                ALTER TABLE commissions 
                ALTER COLUMN order_id DROP NOT NULL;
            """)
            print("      ✅ order_id is now nullable")
        except Exception as e:
            if "already nullable" in str(e).lower():
                print("      ℹ️  order_id is already nullable")
            else:
                print(f"      ❌ Error: {str(e)}")
                return False
        
        # Step 3: Add foreign key constraint for cyber service orders
        print("   Step 3: Adding foreign key constraint...")
        try:
            cursor.execute("""
                ALTER TABLE commissions 
                ADD CONSTRAINT fk_commissions_cyber_service_order
                FOREIGN KEY (cyber_service_order_id) 
                REFERENCES cyber_service_orders(id);
            """)
            print("      ✅ Foreign key constraint added")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("      ℹ️  Foreign key constraint already exists")
            else:
                print(f"      ❌ Error: {str(e)}")
                return False
        
        # Step 4: Add index for performance
        print("   Step 4: Adding performance index...")
        try:
            cursor.execute("""
                CREATE INDEX idx_commissions_cyber_service_order_id 
                ON commissions(cyber_service_order_id);
            """)
            print("      ✅ Performance index added")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("      ℹ️  Performance index already exists")
            else:
                print(f"      ❌ Error: {str(e)}")
        
        cursor.close()
        print(f"\n   🎉 Table structure fixed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error fixing structure: {str(e)}")
        return False

def verify_fix(conn):
    """Verify the fix was successful"""
    
    print(f"\n🔍 VERIFYING THE FIX:")
    print("=" * 50)
    
    try:
        cursor = conn.cursor()
        
        # Check final table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'commissions'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print(f"   Final table structure:")
        for col in columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            print(f"      {col[0]}: {col[1]} {nullable}")
        
        # Check if we can create a test commission record
        print(f"\n   Testing commission creation...")
        
        # Get a sample referrer and cyber service order
        cursor.execute("SELECT id FROM users WHERE referred_by_id IS NOT NULL LIMIT 1;")
        referrer_result = cursor.fetchone()
        
        cursor.execute("SELECT id FROM cyber_service_orders LIMIT 1;")
        order_result = cursor.fetchone()
        
        if referrer_result and order_result:
            referrer_id = referrer_result[0]
            order_id = order_result[0]
            
            print(f"      Test referrer ID: {referrer_id}")
            print(f"      Test order ID: {order_id}")
            
            # Try to insert a test commission
            try:
                cursor.execute("""
                    INSERT INTO commissions (
                        referrer_id, cyber_service_order_id, amount, 
                        commission_type, description, created_at
                    ) VALUES (%s, %s, %s, %s, %s, NOW())
                    RETURNING id;
                """, (referrer_id, order_id, 1.00, 'test', 'Test commission for verification'))
                
                test_commission_id = cursor.fetchone()[0]
                print(f"      ✅ Test commission created with ID: {test_commission_id}")
                
                # Clean up test record
                cursor.execute("DELETE FROM commissions WHERE id = %s;", (test_commission_id,))
                print(f"      🧹 Test commission cleaned up")
                
            except Exception as e:
                print(f"      ❌ Test commission failed: {str(e)}")
                return False
        else:
            print(f"      ⚠️  No test data available for verification")
        
        cursor.close()
        print(f"\n   🎉 Verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Verification failed: {str(e)}")
        return False

def main():
    """Main function to fix the commission table"""
    
    print("🔧 POSTGRESQL COMMISSION TABLE FIX")
    print("=" * 50)
    
    # Connect to database
    conn = get_database_connection()
    if not conn:
        print("❌ Cannot proceed without database connection")
        return
    
    try:
        # Check current structure
        if not check_current_table_structure(conn):
            print("❌ Cannot proceed - table structure check failed")
            return
        
        # Fix the table structure
        if not fix_commission_table_structure(conn):
            print("❌ Table structure fix failed")
            return
        
        # Verify the fix
        if not verify_fix(conn):
            print("❌ Fix verification failed")
            return
        
        print(f"\n🎉 SUCCESS! Commission table structure fixed!")
        print(f"   Your referral system should now work perfectly!")
        print(f"   Test with a small referral payment to verify.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        
    finally:
        if conn:
            conn.close()
            print(f"\n🔌 Database connection closed")

if __name__ == "__main__":
    main() 