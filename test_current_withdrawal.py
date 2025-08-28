#!/usr/bin/env python3
"""
Quick test to verify current withdrawal functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet
from decimal import Decimal

def quick_test():
    """Quick test of withdrawal functionality"""
    print("🧪 Quick Withdrawal Test...")
    
    app = create_app()
    with app.app_context():
        # Get first user
        user = User.query.first()
        if not user:
            print("❌ No users found")
            return
        
        # Ensure wallet exists
        if not user.wallet:
            wallet = Wallet(user_id=user.id)
            db.session.add(wallet)
            db.session.commit()
            user = User.query.get(user.id)
        
        print(f"👤 User: {user.name}")
        print(f"💰 Current balances:")
        print(f"   - Total: KSh {user.wallet.balance}")
        print(f"   - Commission: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited: KSh {user.wallet.deposited_balance}")
        
        # Add some commission
        print(f"\n💸 Adding KSh 50 commission...")
        user.wallet.add_commission(Decimal('50'))
        print(f"   ✅ After commission:")
        print(f"   - Total: KSh {user.wallet.balance}")
        print(f"   - Commission: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited: KSh {user.wallet.deposited_balance}")
        
        # Test withdrawal capability
        print(f"\n💰 Testing withdrawal capability...")
        can_withdraw_30 = user.wallet.can_withdraw(Decimal('30'))
        can_withdraw_100 = user.wallet.can_withdraw(Decimal('100'))
        withdrawable = user.wallet.get_withdrawable_amount()
        
        print(f"   ✅ Can withdraw KSh 30: {can_withdraw_30}")
        print(f"   ✅ Can withdraw KSh 100: {can_withdraw_100}")
        print(f"   ✅ Withdrawable amount: KSh {withdrawable}")
        
        print(f"\n🎉 Test completed!")

if __name__ == "__main__":
    quick_test() 