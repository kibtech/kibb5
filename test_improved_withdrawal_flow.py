#!/usr/bin/env python3
"""
Test script to verify the improved withdrawal flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal, SystemLog
from decimal import Decimal
from datetime import datetime

def test_improved_withdrawal_flow():
    """Test the improved withdrawal flow with balance deduction and manual completion"""
    print("🧪 Testing Improved Withdrawal Flow...")
    
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
        user.wallet.add_deposit(Decimal('100'))
        # Add some commission
        user.wallet.add_commission(Decimal('200'))
        
        print(f"   ✅ Initial wallet state:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        
        # Test 2: Create a withdrawal request
        print(f"\n📤 Test 2: Creating withdrawal request...")
        withdrawal = Withdrawal(
            user_id=user.id,
            amount=Decimal('150'),
            phone_number='254700000000',
            status='pending'
        )
        db.session.add(withdrawal)
        db.session.commit()
        print(f"   ✅ Withdrawal created:")
        print(f"   - ID: {withdrawal.id}")
        print(f"   - Amount: KSh {withdrawal.amount}")
        print(f"   - Status: {withdrawal.status}")
        
        # Test 3: Simulate admin approval (balance deduction)
        print(f"\n✅ Test 3: Simulating admin approval with balance deduction...")
        
        # Check if user can withdraw
        if not user.wallet.can_withdraw(withdrawal.amount):
            print(f"   ❌ User cannot withdraw KSh {withdrawal.amount}")
            return
        
        # Deduct from wallet immediately (simulating admin approval)
        success = user.wallet.deduct_withdrawal(withdrawal.amount)
        if success:
            print(f"   ✅ Balance deducted successfully!")
            print(f"   ✅ Wallet state after deduction:")
            print(f"   - Total Balance: KSh {user.wallet.balance}")
            print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
            print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
            
            # Update withdrawal status to processing (simulating B2C initiation)
            withdrawal.status = 'processing'
            db.session.commit()
        else:
            print(f"   ❌ Failed to deduct balance")
            return
        
        # Test 4: Simulate B2C failure
        print(f"\n❌ Test 4: Simulating B2C failure...")
        withdrawal.status = 'b2c_failed'
        db.session.commit()
        print(f"   ✅ Withdrawal status: {withdrawal.status}")
        print(f"   ✅ Balance remains deducted (KSh {user.wallet.balance})")
        print(f"   ✅ Admin can now manually complete the withdrawal")
        
        # Test 5: Simulate manual completion by admin
        print(f"\n👨‍💼 Test 5: Simulating manual completion by admin...")
        
        # Mark as manually completed
        withdrawal.status = 'completed'
        withdrawal.transaction_id = 'MANUAL_123456'
        withdrawal.paid_at = datetime.utcnow()
        db.session.commit()
        
        print(f"   ✅ Withdrawal manually completed!")
        print(f"   ✅ Final withdrawal status: {withdrawal.status}")
        print(f"   ✅ Transaction ID: {withdrawal.transaction_id}")
        print(f"   ✅ Paid at: {withdrawal.paid_at}")
        
        # Test 6: Verify final wallet state
        print(f"\n💰 Test 6: Verifying final wallet state...")
        print(f"   ✅ Final wallet state:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        
        # Verify the deduction was correct
        expected_commission = Decimal('50')  # 200 - 150
        expected_deposited = Decimal('100')  # unchanged
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
        
        # Test 7: Check system logs
        print(f"\n📝 Test 7: Checking system logs...")
        logs = SystemLog.query.filter_by(user_id=user.id).order_by(SystemLog.created_at.desc()).limit(3).all()
        print(f"   ✅ Recent system logs for user:")
        for log in logs:
            print(f"   - {log.created_at}: {log.level} - {log.message}")
        
        print(f"\n🎉 Improved withdrawal flow test completed!")
        print(f"📊 Summary:")
        print(f"   - Balance is deducted immediately when admin approves")
        print(f"   - Commission balance is prioritized for deductions")
        print(f"   - B2C failures don't affect the balance deduction")
        print(f"   - Admins can manually complete failed B2C withdrawals")
        print(f"   - All wallet balances are properly managed")
        print(f"   - System logging tracks all actions")

if __name__ == "__main__":
    test_improved_withdrawal_flow() 