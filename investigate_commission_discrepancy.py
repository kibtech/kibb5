#!/usr/bin/env python3
"""
Investigate Commission Discrepancy
Analyzes the KSh 1,427 difference between commission records and wallet balances.
"""
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import *
from sqlalchemy import func
from decimal import Decimal

def investigate_commission_discrepancy():
    """Investigate the commission discrepancy found in testing"""
    
    app = create_app()
    
    with app.app_context():
        print("🔍 Commission Discrepancy Investigation")
        print("=" * 50)
        
        # Get the numbers from our test
        total_commission_earned = db.session.query(func.sum(Commission.amount)).scalar() or 0
        total_wallet_balance = db.session.query(func.sum(Wallet.commission_balance)).scalar() or 0
        total_withdrawals = db.session.query(func.sum(Withdrawal.amount)).filter(
            Withdrawal.status == 'approved'
        ).scalar() or 0
        
        print(f"📊 Current Situation:")
        print(f"  💰 Total Commission Records: KSh {total_commission_earned:,.2f}")
        print(f"  💰 Total Wallet Balances: KSh {total_wallet_balance:,.2f}")
        print(f"  💸 Total Approved Withdrawals: KSh {total_withdrawals:,.2f}")
        
        expected_balance = float(total_commission_earned) - float(total_withdrawals)
        actual_balance = float(total_wallet_balance)
        discrepancy = expected_balance - actual_balance
        
        print(f"\n🧮 Calculation:")
        print(f"  Expected Balance = Commission Earned - Withdrawals")
        print(f"  Expected Balance = {total_commission_earned:,.2f} - {total_withdrawals:,.2f}")
        print(f"  Expected Balance = KSh {expected_balance:,.2f}")
        print(f"  Actual Balance = KSh {actual_balance:,.2f}")
        print(f"  📊 Discrepancy = KSh {discrepancy:,.2f}")
        
        print(f"\n🔍 Detailed Analysis:")
        print("=" * 30)
        
        # Check commission records by type
        commission_types = db.session.query(
            Commission.commission_type,
            func.count(Commission.id).label('count'),
            func.sum(Commission.amount).label('total')
        ).group_by(Commission.commission_type).all()
        
        print(f"📋 Commission Records by Type:")
        for comm_type in commission_types:
            print(f"  {comm_type.commission_type}: {comm_type.count} records, KSh {comm_type.total:,.2f}")
        
        # Check for commissions without corresponding wallet updates
        print(f"\n🔍 Checking Commission-Wallet Alignment:")
        
        # Get all commission records with user wallet info
        commission_user_check = db.session.query(
            Commission.referrer_id,
            func.sum(Commission.amount).label('total_commissions')
        ).group_by(Commission.referrer_id).all()
        
        wallet_discrepancies = []
        
        for comm_check in commission_user_check:
            user = db.session.get(User, comm_check.referrer_id)
            if user and user.wallet:
                wallet_balance = float(user.wallet.commission_balance)
                commission_total = float(comm_check.total_commissions)
                
                # Check user's withdrawals
                user_withdrawals = db.session.query(func.sum(Withdrawal.amount)).filter(
                    Withdrawal.user_id == user.id,
                    Withdrawal.status == 'approved'
                ).scalar() or 0
                
                expected_user_balance = commission_total - float(user_withdrawals)
                
                if abs(expected_user_balance - wallet_balance) > 0.01:  # Allow for small rounding
                    discrepancy_amount = expected_user_balance - wallet_balance
                    wallet_discrepancies.append({
                        'user': user,
                        'expected': expected_user_balance,
                        'actual': wallet_balance,
                        'discrepancy': discrepancy_amount,
                        'commissions': commission_total,
                        'withdrawals': float(user_withdrawals)
                    })
        
        if wallet_discrepancies:
            print(f"\n⚠️  Found {len(wallet_discrepancies)} users with wallet discrepancies:")
            total_discrepancy = 0
            for disc in wallet_discrepancies:
                print(f"\n  👤 {disc['user'].name} ({disc['user'].email})")
                print(f"     💰 Commission Records: KSh {disc['commissions']:,.2f}")
                print(f"     💸 Withdrawals: KSh {disc['withdrawals']:,.2f}")
                print(f"     🧮 Expected Wallet: KSh {disc['expected']:,.2f}")
                print(f"     💰 Actual Wallet: KSh {disc['actual']:,.2f}")
                print(f"     📊 Discrepancy: KSh {disc['discrepancy']:,.2f}")
                total_discrepancy += disc['discrepancy']
            
            print(f"\n📊 Total User Discrepancies: KSh {total_discrepancy:,.2f}")
        else:
            print(f"\n✅ No individual user wallet discrepancies found")
        
        # Check for orphaned commission records (referrer doesn't exist)
        print(f"\n🔍 Checking for Orphaned Commission Records:")
        orphaned_commissions = db.session.query(Commission).filter(
            ~Commission.referrer_id.in_(db.session.query(User.id))
        ).all()
        
        if orphaned_commissions:
            orphaned_total = sum(float(comm.amount) for comm in orphaned_commissions)
            print(f"⚠️  Found {len(orphaned_commissions)} orphaned commission records")
            print(f"   Total Amount: KSh {orphaned_total:,.2f}")
            for comm in orphaned_commissions[:5]:  # Show first 5
                print(f"   Commission ID {comm.id}: KSh {comm.amount} for user {comm.referrer_id}")
        else:
            print(f"✅ No orphaned commission records found")
        
        # Check for users with wallets but no commission records
        print(f"\n🔍 Checking Users with Wallet Balance but No Commission Records:")
        users_with_balance = db.session.query(User).join(Wallet).filter(
            Wallet.commission_balance > 0
        ).all()
        
        users_without_records = []
        for user in users_with_balance:
            commission_count = db.session.query(Commission).filter(
                Commission.referrer_id == user.id
            ).count()
            if commission_count == 0:
                users_without_records.append(user)
        
        if users_without_records:
            print(f"⚠️  Found {len(users_without_records)} users with wallet balance but no commission records:")
            for user in users_without_records:
                balance = float(user.wallet.commission_balance)
                print(f"   👤 {user.name}: KSh {balance:,.2f} in wallet, 0 commission records")
        else:
            print(f"✅ All users with wallet balances have corresponding commission records")
        
        # Check withdrawal records validity
        print(f"\n🔍 Checking Withdrawal Record Validity:")
        invalid_withdrawals = db.session.query(Withdrawal).filter(
            ~Withdrawal.user_id.in_(db.session.query(User.id))
        ).all()
        
        if invalid_withdrawals:
            invalid_total = sum(float(w.amount) for w in invalid_withdrawals)
            print(f"⚠️  Found {len(invalid_withdrawals)} withdrawals for non-existent users")
            print(f"   Total Amount: KSh {invalid_total:,.2f}")
        else:
            print(f"✅ All withdrawal records are valid")

def propose_commission_fix():
    """Propose fixes for the commission discrepancy"""
    
    print(f"\n💡 Proposed Solutions:")
    print("=" * 25)
    
    print(f"1. 🔧 **Data Cleanup Options:**")
    print(f"   a) Remove orphaned commission records")
    print(f"   b) Create commission records for users with balances but no records")
    print(f"   c) Recalculate all wallet balances from commission records")
    print(f"   d) Audit and fix individual user discrepancies")
    
    print(f"\n2. 🛠️ **System Improvements:**")
    print(f"   a) Add database constraints to prevent orphaned records")
    print(f"   b) Implement wallet balance validation triggers")
    print(f"   c) Add commission-wallet consistency checks")
    print(f"   d) Create automated reconciliation process")
    
    print(f"\n3. ⚡ **Immediate Actions:**")
    print(f"   a) Backup current database state")
    print(f"   b) Run detailed discrepancy analysis")
    print(f"   c) Fix high-priority discrepancies first")
    print(f"   d) Implement monitoring for future consistency")
    
    print(f"\n4. 📊 **Analytics Adjustments:**")
    print(f"   a) Add discrepancy detection to analytics")
    print(f"   b) Show data quality indicators")
    print(f"   c) Alert on inconsistencies")
    print(f"   d) Provide reconciliation tools")

if __name__ == "__main__":
    print("🚀 Commission Discrepancy Investigation")
    print("-" * 50)
    
    investigate_commission_discrepancy()
    propose_commission_fix()
    
    print(f"\n📋 Next Steps:")
    print("=" * 15)
    print("1. Review discrepancy details above")
    print("2. Choose appropriate fix strategy")
    print("3. Backup database before making changes")
    print("4. Implement fixes gradually with testing")
    print("5. Add monitoring to prevent future issues")
    
    print("\n✅ Investigation completed!")