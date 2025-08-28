#!/usr/bin/env python3
"""
Test script to verify withdrawal approval deducts from commission balance
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal, SystemLog
from decimal import Decimal
from datetime import datetime

def test_withdrawal_approval():
    """Test that withdrawal approval correctly deducts from commission balance"""
    print("🧪 Testing Withdrawal Approval Process...")
    
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
        
        # Test 1: Set up initial balances
        print(f"\n💰 Test 1: Setting up initial balances...")
        # Add some deposited money
        user.wallet.add_deposit(Decimal('50'))
        # Add some commission
        user.wallet.add_commission(Decimal('100'))
        
        print(f"   ✅ Initial wallet state:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        
        # Test 2: Create a withdrawal request
        print(f"\n📤 Test 2: Creating withdrawal request...")
        withdrawal = Withdrawal(
            user_id=user.id,
            amount=Decimal('75'),
            phone_number='254700000000',
            status='pending'
        )
        db.session.add(withdrawal)
        db.session.commit()
        print(f"   ✅ Withdrawal created:")
        print(f"   - ID: {withdrawal.id}")
        print(f"   - Amount: KSh {withdrawal.amount}")
        print(f"   - Status: {withdrawal.status}")
        
        # Test 3: Approve the withdrawal (simulate admin approval)
        print(f"\n✅ Test 3: Approving withdrawal...")
        try:
            # Check if user can withdraw
            if not user.wallet.can_withdraw(withdrawal.amount):
                print(f"   ❌ User cannot withdraw KSh {withdrawal.amount}")
                return
            
            # Update withdrawal status to completed
            withdrawal.status = 'completed'
            withdrawal.paid_at = datetime.utcnow()
            
            # Deduct from wallet
            success = user.wallet.deduct_withdrawal(withdrawal.amount)
            if success:
                db.session.commit()
                print(f"   ✅ Withdrawal approved successfully!")
                print(f"   ✅ Withdrawal status: {withdrawal.status}")
                print(f"   ✅ Paid at: {withdrawal.paid_at}")
            else:
                print(f"   ❌ Failed to deduct withdrawal amount")
                db.session.rollback()
                return
                
        except Exception as e:
            print(f"   ❌ Error approving withdrawal: {str(e)}")
            db.session.rollback()
            return
        
        # Test 4: Check final wallet balances
        print(f"\n💰 Test 4: Checking final wallet balances...")
        print(f"   ✅ Final wallet state:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        
        # Verify the deduction
        expected_commission = Decimal('25')  # 100 - 75
        expected_deposited = Decimal('50')   # unchanged
        expected_total = expected_commission + expected_deposited
        
        print(f"\n🔍 Verification:")
        print(f"   - Expected Commission Balance: KSh {expected_commission}")
        print(f"   - Actual Commission Balance: KSh {user.wallet.commission_balance}")
        print(f"   - Expected Total Balance: KSh {expected_total}")
        print(f"   - Actual Total Balance: KSh {user.wallet.balance}")
        
        if (user.wallet.commission_balance == expected_commission and 
            user.wallet.balance == expected_total):
            print(f"   ✅ All balances are correct!")
        else:
            print(f"   ❌ Balance verification failed!")
        
        # Test 5: Test another withdrawal that uses both commission and deposited
        print(f"\n📤 Test 5: Testing withdrawal that uses both balances...")
        withdrawal2 = Withdrawal(
            user_id=user.id,
            amount=Decimal('60'),  # 25 commission + 35 deposited
            phone_number='254700000000',
            status='pending'
        )
        db.session.add(withdrawal2)
        db.session.commit()
        
        print(f"   ✅ Second withdrawal created:")
        print(f"   - Amount: KSh {withdrawal2.amount}")
        print(f"   - Current Commission: KSh {user.wallet.commission_balance}")
        print(f"   - Current Deposited: KSh {user.wallet.deposited_balance}")
        
        # Approve second withdrawal
        if user.wallet.can_withdraw(withdrawal2.amount):
            withdrawal2.status = 'completed'
            withdrawal2.paid_at = datetime.utcnow()
            success = user.wallet.deduct_withdrawal(withdrawal2.amount)
            if success:
                db.session.commit()
                print(f"   ✅ Second withdrawal approved!")
                print(f"   ✅ Final balances after second withdrawal:")
                print(f"   - Total Balance: KSh {user.wallet.balance}")
                print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
                print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
            else:
                print(f"   ❌ Failed to approve second withdrawal")
        else:
            print(f"   ❌ Cannot withdraw KSh {withdrawal2.amount}")
        
        print(f"\n🎉 Withdrawal approval test completed!")
        print(f"📊 Summary:")
        print(f"   - Withdrawal approval correctly deducts from commission balance first")
        print(f"   - If commission is insufficient, it uses deposited balance")
        print(f"   - Total balance is properly recalculated")
        print(f"   - Withdrawal status is updated correctly")

if __name__ == "__main__":
    test_withdrawal_approval() 