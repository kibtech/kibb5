#!/usr/bin/env python3
"""
Script to manage pending withdrawals for Duke Willer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Withdrawal
from decimal import Decimal
from datetime import datetime

def manage_pending_withdrawals():
    """Manage pending withdrawals for Duke Willer"""
    print("🔄 Managing Pending Withdrawals for Duke Willer...")
    
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
        
        # Get all pending withdrawals
        pending_withdrawals = Withdrawal.query.filter_by(
            user_id=user.id, 
            status='pending'
        ).order_by(Withdrawal.requested_at.asc()).all()
        
        print(f"\n📤 Found {len(pending_withdrawals)} pending withdrawals:")
        
        total_requested = Decimal('0')
        for i, withdrawal in enumerate(pending_withdrawals, 1):
            total_requested += withdrawal.amount
            print(f"   {i:2d}. ID: {withdrawal.id:2d} | KSh {withdrawal.amount:6.2f} | {withdrawal.requested_at.strftime('%Y-%m-%d %H:%M')}")
        
        print(f"\n💰 Total Requested: KSh {total_requested}")
        print(f"💰 Available Balance: KSh {user.wallet.balance}")
        
        if total_requested > user.wallet.balance:
            print(f"⚠️  WARNING: Total requested ({total_requested}) exceeds available balance ({user.wallet.balance})")
            print(f"   This means some withdrawals cannot be processed!")
        
        # Show options
        print(f"\n🎯 Management Options:")
        print(f"   1. Approve all withdrawals (if balance allows)")
        print(f"   2. Approve withdrawals one by one")
        print(f"   3. Reject all withdrawals")
        print(f"   4. Approve only the oldest withdrawal")
        print(f"   5. Show detailed withdrawal info")
        print(f"   6. Exit")
        
        while True:
            try:
                choice = input(f"\nEnter your choice (1-6): ").strip()
                
                if choice == '1':
                    approve_all_withdrawals(user, pending_withdrawals)
                    break
                elif choice == '2':
                    approve_withdrawals_one_by_one(user, pending_withdrawals)
                    break
                elif choice == '3':
                    reject_all_withdrawals(pending_withdrawals)
                    break
                elif choice == '4':
                    if pending_withdrawals:
                        approve_single_withdrawal(user, pending_withdrawals[0])
                    break
                elif choice == '5':
                    show_detailed_withdrawals(pending_withdrawals)
                    continue
                elif choice == '6':
                    print("👋 Exiting...")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-6.")
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break

def approve_all_withdrawals(user, withdrawals):
    """Approve all withdrawals if balance allows"""
    print(f"\n✅ Approving all withdrawals...")
    
    total_amount = sum(w.amount for w in withdrawals)
    if total_amount > user.wallet.balance:
        print(f"❌ Cannot approve all: Total ({total_amount}) > Balance ({user.wallet.balance})")
        return
    
    approved_count = 0
    for withdrawal in withdrawals:
        try:
            # Simulate admin approval
            success = user.wallet.deduct_withdrawal(withdrawal.amount)
            if success:
                withdrawal.status = 'completed'
                withdrawal.transaction_id = f'BATCH_APPROVAL_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
                withdrawal.paid_at = datetime.utcnow()
                approved_count += 1
                print(f"   ✅ Approved withdrawal {withdrawal.id}: KSh {withdrawal.amount}")
            else:
                print(f"   ❌ Failed to approve withdrawal {withdrawal.id}: KSh {withdrawal.amount}")
        except Exception as e:
            print(f"   ❌ Error approving withdrawal {withdrawal.id}: {str(e)}")
    
    db.session.commit()
    print(f"\n🎉 Successfully approved {approved_count}/{len(withdrawals)} withdrawals!")

def approve_withdrawals_one_by_one(user, withdrawals):
    """Approve withdrawals one by one"""
    print(f"\n✅ Approving withdrawals one by one...")
    
    for i, withdrawal in enumerate(withdrawals, 1):
        print(f"\n📤 Withdrawal {i}/{len(withdrawals)}:")
        print(f"   ID: {withdrawal.id}")
        print(f"   Amount: KSh {withdrawal.amount}")
        print(f"   Requested: {withdrawal.requested_at}")
        print(f"   Phone: {withdrawal.phone_number}")
        
        if withdrawal.amount > user.wallet.balance:
            print(f"   ❌ Cannot approve: Amount ({withdrawal.amount}) > Balance ({user.wallet.balance})")
            continue
        
        choice = input(f"   Approve this withdrawal? (y/n/skip): ").strip().lower()
        
        if choice == 'y':
            try:
                success = user.wallet.deduct_withdrawal(withdrawal.amount)
                if success:
                    withdrawal.status = 'completed'
                    withdrawal.transaction_id = f'MANUAL_APPROVAL_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
                    withdrawal.paid_at = datetime.utcnow()
                    db.session.commit()
                    print(f"   ✅ Approved!")
                else:
                    print(f"   ❌ Failed to deduct amount")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        elif choice == 'skip':
            print(f"   ⏭️  Skipped")
        else:
            print(f"   ❌ Rejected")

def reject_all_withdrawals(withdrawals):
    """Reject all withdrawals"""
    print(f"\n❌ Rejecting all withdrawals...")
    
    for withdrawal in withdrawals:
        withdrawal.status = 'failed'
        print(f"   ❌ Rejected withdrawal {withdrawal.id}: KSh {withdrawal.amount}")
    
    db.session.commit()
    print(f"\n🎉 Successfully rejected {len(withdrawals)} withdrawals!")

def approve_single_withdrawal(user, withdrawal):
    """Approve a single withdrawal"""
    print(f"\n✅ Approving single withdrawal...")
    print(f"   ID: {withdrawal.id}")
    print(f"   Amount: KSh {withdrawal.amount}")
    print(f"   Requested: {withdrawal.requested_at}")
    
    if withdrawal.amount > user.wallet.balance:
        print(f"   ❌ Cannot approve: Amount ({withdrawal.amount}) > Balance ({user.wallet.balance})")
        return
    
    try:
        success = user.wallet.deduct_withdrawal(withdrawal.amount)
        if success:
            withdrawal.status = 'completed'
            withdrawal.transaction_id = f'SINGLE_APPROVAL_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
            withdrawal.paid_at = datetime.utcnow()
            db.session.commit()
            print(f"   ✅ Approved successfully!")
        else:
            print(f"   ❌ Failed to deduct amount")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def show_detailed_withdrawals(withdrawals):
    """Show detailed information about withdrawals"""
    print(f"\n📊 Detailed Withdrawal Information:")
    for i, withdrawal in enumerate(withdrawals, 1):
        print(f"\n   {i}. Withdrawal ID: {withdrawal.id}")
        print(f"      Amount: KSh {withdrawal.amount}")
        print(f"      Phone: {withdrawal.phone_number}")
        print(f"      Status: {withdrawal.status}")
        print(f"      Requested: {withdrawal.requested_at}")
        if withdrawal.paid_at:
            print(f"      Paid: {withdrawal.paid_at}")
        if withdrawal.transaction_id:
            print(f"      Transaction ID: {withdrawal.transaction_id}")

if __name__ == "__main__":
    manage_pending_withdrawals() 