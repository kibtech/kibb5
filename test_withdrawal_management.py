#!/usr/bin/env python3
"""
Test script to verify withdrawal management system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal
from decimal import Decimal
from datetime import datetime

def test_withdrawal_management():
    """Test the withdrawal management system"""
    print("🧪 Testing Withdrawal Management System...")
    
    app = create_app()
    with app.app_context():
        # Test 1: Check if Duke Willer exists and has withdrawals
        user = User.query.filter_by(name='Duke Willer').first()
        if not user:
            print("❌ User 'Duke Willer' not found")
            return
        
        print(f"✅ User found: {user.name} ({user.email})")
        print(f"💰 Wallet Balance: KSh {user.wallet.balance}")
        
        # Test 2: Count pending withdrawals
        pending_withdrawals = Withdrawal.query.filter_by(
            user_id=user.id, 
            status='pending'
        ).count()
        
        print(f"📤 Pending Withdrawals: {pending_withdrawals}")
        
        # Test 3: Show withdrawal status breakdown
        status_counts = db.session.query(
            Withdrawal.status, 
            db.func.count(Withdrawal.id)
        ).filter_by(user_id=user.id).group_by(Withdrawal.status).all()
        
        print(f"\n📊 Withdrawal Status Breakdown:")
        for status, count in status_counts:
            print(f"   - {status}: {count}")
        
        # Test 4: Show oldest pending withdrawal
        oldest_pending = Withdrawal.query.filter_by(
            user_id=user.id, 
            status='pending'
        ).order_by(Withdrawal.requested_at.asc()).first()
        
        if oldest_pending:
            print(f"\n📤 Oldest Pending Withdrawal:")
            print(f"   ID: {oldest_pending.id}")
            print(f"   Amount: KSh {oldest_pending.amount}")
            print(f"   Requested: {oldest_pending.requested_at}")
            print(f"   Phone: {oldest_pending.phone_number}")
        else:
            print(f"\n✅ No pending withdrawals found")
        
        # Test 5: Check if user can withdraw
        if user.wallet:
            can_withdraw = user.wallet.can_withdraw(Decimal('10'))
            print(f"\n💳 Can withdraw KSh 10: {can_withdraw}")
            
            if hasattr(user.wallet, 'has_pending_withdrawal'):
                has_pending = user.wallet.has_pending_withdrawal()
                print(f"📤 Has pending withdrawal: {has_pending}")
        
        print(f"\n🎉 Withdrawal management test completed!")
        print(f"\n📋 Next Steps:")
        print(f"   1. Access admin panel: https://kibtech.coke/admin")
        print(f"   2. Go to User Management → Withdrawal Requests")
        print(f"   3. Or use the management script: python manage_pending_withdrawals.py")

if __name__ == "__main__":
    test_withdrawal_management() 