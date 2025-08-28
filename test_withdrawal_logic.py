#!/usr/bin/env python3
"""
Test Withdrawal Logic
=====================
Test the updated withdrawal logic that allows withdrawals from both
commission and deposited balances.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, SystemSettings
from decimal import Decimal

def test_withdrawal_logic():
    """Test the withdrawal logic with different balance scenarios"""
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Testing Withdrawal Logic")
        print("=" * 50)
        
        # Find the test user
        user = User.query.filter_by(email='kashdyke@gmail.com').first()
        if not user:
            print("❌ User not found")
            return
        
        wallet = user.wallet
        if not wallet:
            print("❌ Wallet not found")
            return
        
        print(f"👤 User: {user.name} ({user.email})")
        print(f"💰 Current balances:")
        print(f"   - Total Balance: KSh {wallet.balance}")
        print(f"   - Deposited Balance: KSh {wallet.deposited_balance}")
        print(f"   - Commission Balance: KSh {wallet.commission_balance}")
        print(f"   - Withdrawable Balance: KSh {wallet.get_withdrawable_amount()}")
        
        # Test withdrawal scenarios
        test_amounts = [10, 25, 50, 100]
        
        for amount in test_amounts:
            print(f"\n🧪 Testing withdrawal of KSh {amount}:")
            
            can_withdraw = wallet.can_withdraw(amount)
            withdrawable = wallet.get_withdrawable_amount()
            
            print(f"   - Can withdraw KSh {amount}: {can_withdraw}")
            print(f"   - Available for withdrawal: KSh {withdrawable}")
            
            if can_withdraw:
                print(f"   - ✅ Withdrawal of KSh {amount} is possible")
            else:
                print(f"   - ❌ Withdrawal of KSh {amount} is not possible")
        
        # Test the deduct_withdrawal method
        print(f"\n🧪 Testing deduct_withdrawal method:")
        
        # Save original balances
        original_commission = wallet.commission_balance
        original_deposited = wallet.deposited_balance
        original_total = wallet.balance
        
        # Test withdrawal of 10
        test_amount = Decimal('10.00')
        print(f"   - Attempting to withdraw KSh {test_amount}")
        
        success = wallet.deduct_withdrawal(test_amount)
        
        if success:
            print(f"   - ✅ Withdrawal successful!")
            print(f"   - Commission balance: KSh {original_commission} → KSh {wallet.commission_balance}")
            print(f"   - Deposited balance: KSh {original_deposited} → KSh {wallet.deposited_balance}")
            print(f"   - Total balance: KSh {original_total} → KSh {wallet.balance}")
        else:
            print(f"   - ❌ Withdrawal failed!")
        
        print(f"\n✅ Withdrawal logic test completed!")

if __name__ == "__main__":
    test_withdrawal_logic() 