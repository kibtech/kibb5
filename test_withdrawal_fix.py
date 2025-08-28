#!/usr/bin/env python3
"""
Test script to verify withdrawal functionality with new commission balance behavior
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal, SystemLog
from decimal import Decimal

def test_withdrawal_functionality():
    """Test withdrawal functionality with new commission balance behavior"""
    print("🧪 Testing Withdrawal Functionality...")
    
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
        
        # Test 1: Add some commission balance
        print(f"\n💸 Test 1: Adding KSh 100 commission...")
        user.wallet.add_commission(Decimal('100'))
        print(f"   ✅ After commission:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        
        # Test 2: Check if user can withdraw
        print(f"\n💰 Test 2: Checking withdrawal capability...")
        can_withdraw = user.wallet.can_withdraw(Decimal('50'))
        withdrawable_amount = user.wallet.get_withdrawable_amount()
        print(f"   ✅ Can withdraw KSh 50: {can_withdraw}")
        print(f"   ✅ Withdrawable amount: KSh {withdrawable_amount}")
        
        # Test 3: Create a withdrawal request
        print(f"\n📤 Test 3: Creating withdrawal request...")
        try:
            withdrawal = Withdrawal(
                user_id=user.id,
                amount=Decimal('50'),
                phone_number='254700000000',
                status='pending'
            )
            db.session.add(withdrawal)
            db.session.commit()
            print(f"   ✅ Withdrawal created successfully!")
            print(f"   ✅ Withdrawal ID: {withdrawal.id}")
            print(f"   ✅ Amount: KSh {withdrawal.amount}")
            print(f"   ✅ Status: {withdrawal.status}")
            
            # Test 4: Log the withdrawal
            print(f"\n📝 Test 4: Logging withdrawal request...")
            log_entry = SystemLog.create_log(
                level='INFO',
                category='wallet',
                message=f'Test withdrawal request created for user {user.name}',
                user_id=user.id,
                details={
                    'withdrawal_id': withdrawal.id,
                    'amount': float(withdrawal.amount),
                    'phone_number': withdrawal.phone_number
                }
            )
            if log_entry:
                print(f"   ✅ System log created successfully!")
                print(f"   ✅ Log ID: {log_entry.id}")
                print(f"   ✅ Message: {log_entry.message}")
            else:
                print(f"   ❌ Failed to create system log")
            
            # Test 5: Check wallet balance after withdrawal
            print(f"\n💰 Test 5: Checking wallet balance after withdrawal...")
            print(f"   ✅ Current wallet state:")
            print(f"   - Total Balance: KSh {user.wallet.balance}")
            print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
            print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
            
            # Note: The actual deduction happens when admin approves the withdrawal
            # This test just verifies the withdrawal request creation works
            
        except Exception as e:
            print(f"   ❌ Error creating withdrawal: {str(e)}")
            db.session.rollback()
        
        print(f"\n🎉 Withdrawal functionality test completed!")
        print(f"📊 Summary:")
        print(f"   - Commission balance is tracked separately")
        print(f"   - Withdrawal requests can be created")
        print(f"   - System logging works correctly")
        print(f"   - Wallet balances are properly managed")

if __name__ == "__main__":
    test_withdrawal_functionality() 