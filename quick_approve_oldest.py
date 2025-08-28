#!/usr/bin/env python3
"""
Quick script to approve the oldest pending withdrawal for Duke Willer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal
from decimal import Decimal
from datetime import datetime

def quick_approve_oldest():
    """Quickly approve the oldest pending withdrawal"""
    print("⚡ Quick Approve Oldest Withdrawal...")
    
    app = create_app()
    with app.app_context():
        # Find the user (Duke Willer)
        user = User.query.filter_by(name='Duke Willer').first()
        if not user:
            print("❌ User 'Duke Willer' not found")
            return
        
        print(f"👤 User: {user.name} ({user.email})")
        print(f"💰 Current Balance: KSh {user.wallet.balance}")
        
        # Find oldest pending withdrawal
        oldest_withdrawal = Withdrawal.query.filter_by(
            user_id=user.id, 
            status='pending'
        ).order_by(Withdrawal.requested_at.asc()).first()
        
        if not oldest_withdrawal:
            print("❌ No pending withdrawals found")
            return
        
        print(f"\n📤 Oldest Pending Withdrawal:")
        print(f"   ID: {oldest_withdrawal.id}")
        print(f"   Amount: KSh {oldest_withdrawal.amount}")
        print(f"   Requested: {oldest_withdrawal.requested_at}")
        print(f"   Phone: {oldest_withdrawal.phone_number}")
        
        if oldest_withdrawal.amount > user.wallet.balance:
            print(f"\n❌ Cannot approve: Amount ({oldest_withdrawal.amount}) > Balance ({user.wallet.balance})")
            return
        
        # Auto-approve
        try:
            success = user.wallet.deduct_withdrawal(oldest_withdrawal.amount)
            if success:
                oldest_withdrawal.status = 'completed'
                oldest_withdrawal.transaction_id = f'QUICK_APPROVAL_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
                oldest_withdrawal.paid_at = datetime.utcnow()
                db.session.commit()
                
                print(f"\n✅ SUCCESS! Withdrawal approved!")
                print(f"   - Status: {oldest_withdrawal.status}")
                print(f"   - Transaction ID: {oldest_withdrawal.transaction_id}")
                print(f"   - New Balance: KSh {user.wallet.balance}")
                print(f"   - Remaining Pending: {Withdrawal.query.filter_by(user_id=user.id, status='pending').count()}")
            else:
                print(f"\n❌ Failed to deduct amount from wallet")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    quick_approve_oldest() 