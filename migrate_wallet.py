#!/usr/bin/env python3
"""
Migration script to add deposited_balance and commission_balance columns to wallets table
"""

import os
import sys
from app import create_app, db
from app.models import Wallet
from decimal import Decimal

def migrate_wallet_structure():
    """Migrate wallet structure to support separate deposited and commission balances"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add new columns if they don't exist
            print("🔄 Adding new wallet columns...")
            
            # Check if columns exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('wallets')]
            
            if 'deposited_balance' not in columns:
                db.engine.execute('ALTER TABLE wallets ADD COLUMN deposited_balance NUMERIC(10, 2) DEFAULT 0.0 NOT NULL')
                print("✅ Added deposited_balance column")
            
            if 'commission_balance' not in columns:
                db.engine.execute('ALTER TABLE wallets ADD COLUMN commission_balance NUMERIC(10, 2) DEFAULT 0.0 NOT NULL')
                print("✅ Added commission_balance column")
            
            # Migrate existing data
            print("🔄 Migrating existing wallet data...")
            wallets = Wallet.query.all()
            
            for wallet in wallets:
                # Move existing balance to commission_balance (assuming it's commission)
                if wallet.commission_balance == 0 and wallet.balance > 0:
                    wallet.commission_balance = wallet.balance
                    wallet.deposited_balance = 0
                    print(f"✅ Migrated wallet {wallet.id}: {wallet.balance} → commission_balance")
            
            db.session.commit()
            print("✅ Wallet migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_wallet_structure() 