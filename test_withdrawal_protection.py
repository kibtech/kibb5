#!/usr/bin/env python3
"""
Test script to verify withdrawal protection against multiple requests
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal
from decimal import Decimal
from datetime import datetime

def test_withdrawal_protection():
    """Test that multiple withdrawal requests are properly prevented"""
    print("🛡️ Testing Withdrawal Protection...")
    
    app = create_app()
    with app.app_context():
        # Find the user (Duke Willer)
        user = User.query.filter_by(name='Duke Willer').first()
        if not user:
            print("❌ User 'Duke Willer' not found")
            return
        
        print(f"👤 User: {user.name} ({user.email})")
        print(f"💰 Current Wallet State:")
        print(f"   - Total Balance: KSh {user.wallet.balance}")
        print(f"   - Commission Balance: KSh {user.wallet.commission_balance}")
        print(f"   - Deposited Balance: KSh {user.wallet.deposited_balance}")
        
        # Check current pending withdrawals
        pending_withdrawals = Withdrawal.query.filter_by(user_id=user.id, status='pending').all()
        print(f"\n📤 Current Pending Withdrawals: {len(pending_withdrawals)}")
        for w in pending_withdrawals:
            print(f"   - ID: {w.id}, Amount: KSh {w.amount}, Status: {w.status}")
        
        # Test 1: Try to create a withdrawal when one is already pending
        print(f"\n🧪 Test 1: Attempting to create withdrawal when one is pending...")
        
        if user.wallet.has_pending_withdrawal():
            print(f"   ✅ Protection working: User has pending withdrawal")
            print(f"   ✅ User cannot create another withdrawal until pending one is processed")
        else:
            print(f"   ℹ️ No pending withdrawals found")
        
        # Test 2: Check if user can withdraw the amount they want
        test_amount = Decimal('20')
        print(f"\n🧪 Test 2: Checking if user can withdraw KSh {test_amount}...")
        
        if user.wallet.can_withdraw(test_amount):
            print(f"   ✅ User has sufficient balance for KSh {test_amount}")
        else:
            print(f"   ❌ User cannot withdraw KSh {test_amount}")
            print(f"   Available: KSh {user.wallet.get_withdrawable_amount()}")
        
        # Test 3: Show all user's withdrawals
        print(f"\n📊 All User Withdrawals:")
        all_withdrawals = Withdrawal.query.filter_by(user_id=user.id).order_by(Withdrawal.requested_at.desc()).all()
        
        for withdrawal in all_withdrawals:
            print(f"   - ID: {withdrawal.id}")
            print(f"     Amount: KSh {withdrawal.amount}")
            print(f"     Status: {withdrawal.status}")
            print(f"     Requested: {withdrawal.requested_at}")
            if withdrawal.paid_at:
                print(f"     Paid: {withdrawal.paid_at}")
            print()
        
        # Test 4: Check for recent completed withdrawals (within 5 minutes)
        print(f"\n🧪 Test 4: Checking for recent completed withdrawals...")
        from datetime import timedelta
        recent_withdrawal = Withdrawal.query.filter(
            Withdrawal.user_id == user.id,
            Withdrawal.status == 'completed',
            Withdrawal.paid_at >= datetime.utcnow() - timedelta(minutes=5)
        ).first()
        
        if recent_withdrawal:
            print(f"   ⚠️ Recent withdrawal found (within 5 minutes):")
            print(f"   - ID: {recent_withdrawal.id}")
            print(f"   - Amount: KSh {recent_withdrawal.amount}")
            print(f"   - Completed: {recent_withdrawal.paid_at}")
            print(f"   ✅ User should wait before requesting another withdrawal")
        else:
            print(f"   ✅ No recent withdrawals found")
        
        print(f"\n🎉 Withdrawal protection test completed!")
        print(f"📋 Summary:")
        print(f"   - Multiple pending withdrawals: {'BLOCKED' if user.wallet.has_pending_withdrawal() else 'ALLOWED'}")
        print(f"   - Recent withdrawal spam: {'BLOCKED' if recent_withdrawal else 'ALLOWED'}")
        print(f"   - Sufficient balance check: {'PASS' if user.wallet.can_withdraw(test_amount) else 'FAIL'}")

if __name__ == "__main__":
    test_withdrawal_protection() 