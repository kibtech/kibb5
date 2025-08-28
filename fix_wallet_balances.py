#!/usr/bin/env python3
"""
Script to fix all wallet balances by recalculating them
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet
from decimal import Decimal

def fix_wallet_balances():
    """Fix all wallet balances by recalculating them"""
    print("🔧 Fixing Wallet Balances...")
    
    app = create_app()
    with app.app_context():
        # Get all wallets
        wallets = Wallet.query.all()
        print(f"📊 Found {len(wallets)} wallets to fix")
        
        fixed_count = 0
        for wallet in wallets:
            # Calculate what the balance should be
            correct_balance = wallet.deposited_balance + wallet.commission_balance
            current_balance = wallet.balance
            
            if current_balance != correct_balance:
                print(f"🔧 Fixing wallet {wallet.id} (User: {wallet.user.name}):")
                print(f"   - Current balance: KSh {current_balance}")
                print(f"   - Deposited: KSh {wallet.deposited_balance}")
                print(f"   - Commission: KSh {wallet.commission_balance}")
                print(f"   - Correct balance: KSh {correct_balance}")
                
                # Fix the balance
                wallet.balance = correct_balance
                fixed_count += 1
            else:
                print(f"✅ Wallet {wallet.id} (User: {wallet.user.name}) is already correct")
        
        # Commit all changes
        if fixed_count > 0:
            db.session.commit()
            print(f"\n🎉 Fixed {fixed_count} wallet balances!")
        else:
            print(f"\n✅ All wallet balances are already correct!")
        
        # Verify the fix
        print(f"\n🔍 Verification:")
        wallets = Wallet.query.all()
        for wallet in wallets:
            correct_balance = wallet.deposited_balance + wallet.commission_balance
            if wallet.balance == correct_balance:
                print(f"✅ Wallet {wallet.id}: KSh {wallet.balance} (correct)")
            else:
                print(f"❌ Wallet {wallet.id}: KSh {wallet.balance} (should be KSh {correct_balance})")

if __name__ == "__main__":
    fix_wallet_balances() 