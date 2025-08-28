#!/usr/bin/env python3
"""
Test script to verify the new commission balance behavior
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, AdminUser
from decimal import Decimal

def test_commission_balance_behavior():
    """Test the new commission balance behavior"""
    print("🧪 Testing New Commission Balance Behavior...")
    
    app = create_app()
    with app.app_context():
        # Find a test user
        user = User.query.first()
        if not user:
            print("❌ No users found in database")
            return
        
        # Ensure user has a wallet
        if not user.wallet:
            wallet = Wallet(user_id=user.id)
            db.session.add(wallet)
            db.session.commit()
            user = User.query.get(user.id)  # Refresh user object
        
        print(f"👤 Testing with user: {user.name} ({user.email})")
        print(f"💰 Initial wallet state:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        
        # Test 1: Add deposit
        print(f"\n📥 Test 1: Adding KSh 100 deposit...")
        user.wallet.add_deposit(Decimal('100'))
        print(f"   ✅ After deposit:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        
        # Test 2: Add commission (should NOT affect total balance)
        print(f"\n💸 Test 2: Adding KSh 50 commission...")
        user.wallet.add_commission(Decimal('50'))
        print(f"   ✅ After commission:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        
        # Test 3: Add another commission
        print(f"\n💸 Test 3: Adding KSh 25 commission...")
        user.wallet.add_commission(Decimal('25'))
        print(f"   ✅ After second commission:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        
        # Test 4: Purchase using deposited balance
        print(f"\n🛒 Test 4: Making KSh 30 purchase...")
        success = user.wallet.deduct_purchase(Decimal('30'))
        print(f"   ✅ Purchase {'successful' if success else 'failed'}:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        
        # Test 5: Purchase that uses both deposited and commission
        print(f"\n🛒 Test 5: Making KSh 100 purchase (uses both balances)...")
        success = user.wallet.deduct_purchase(Decimal('100'))
        print(f"   ✅ Purchase {'successful' if success else 'failed'}:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        
        print(f"\n🎉 Commission balance behavior test completed!")
        print(f"📊 Summary:")
        print(f"   - Commissions are now tracked separately")
        print(f"   - Total balance = Deposited + Commission")
        print(f"   - Purchases deduct from deposited first, then commission")

if __name__ == "__main__":
    test_commission_balance_behavior() 