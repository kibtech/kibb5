import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def fix_wallet_schema():
    """Fix the wallet table schema by adding missing columns"""
    print("🔧 Fixing Wallet Table Schema...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if deposited_balance column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'wallets' 
                AND column_name = 'deposited_balance'
            """))
            
            if result.fetchone():
                print("✅ deposited_balance column already exists")
            else:
                print("📝 Adding deposited_balance column...")
                db.session.execute(text("""
                    ALTER TABLE wallets 
                    ADD COLUMN deposited_balance NUMERIC(10,2) DEFAULT 0.0 NOT NULL
                """))
                db.session.commit()
                print("✅ deposited_balance column added successfully")
            
            # Check if commission_balance column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'wallets' 
                AND column_name = 'commission_balance'
            """))
            
            if result.fetchone():
                print("✅ commission_balance column already exists")
            else:
                print("📝 Adding commission_balance column...")
                db.session.execute(text("""
                    ALTER TABLE wallets 
                    ADD COLUMN commission_balance NUMERIC(10,2) DEFAULT 0.0 NOT NULL
                """))
                db.session.commit()
                print("✅ commission_balance column added successfully")
            
            # Update existing wallets to have proper values
            print("🔄 Updating existing wallet records...")
            db.session.execute(text("""
                UPDATE wallets 
                SET deposited_balance = balance 
                WHERE deposited_balance IS NULL OR deposited_balance = 0
            """))
            db.session.commit()
            print("✅ Wallet records updated")
            
            print("\n🎉 Wallet schema fix completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing wallet schema: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🚀 Wallet Schema Fix Tool")
    print("=" * 50)
    
    success = fix_wallet_schema()
    
    if success:
        print("\n✅ Wallet schema is now compatible with the application!")
        print("💡 You can now run the application without database errors.")
    else:
        print("\n❌ Failed to fix wallet schema. Please check the error above.") 