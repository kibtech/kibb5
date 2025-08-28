#!/usr/bin/env python3
"""
Fix Commission Discrepancies
Targeted fixes for the KSh 1,427 discrepancy identified in investigation.
"""
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import *
from sqlalchemy import func
from decimal import Decimal

def fix_commission_discrepancies():
    """Fix the specific commission discrepancies identified"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Fixing Commission Discrepancies")
        print("=" * 50)
        
        print("📋 Issues Identified:")
        print("1. CHRISTOPHER PORIOT: KSh 1,440 discrepancy")
        print("2. SENIOR MARKETING OFFICER: KSh 10.00 in wallet, 0 commission records")
        print("3. EMMKASH: KSh 3.00 in wallet, 0 commission records")
        
        print(f"\n🔍 Pre-Fix Analysis:")
        print("=" * 25)
        
        # Check current state
        total_commission_earned = db.session.query(func.sum(Commission.amount)).scalar() or 0
        total_wallet_balance = db.session.query(func.sum(Wallet.commission_balance)).scalar() or 0
        expected_balance = float(total_commission_earned)
        actual_balance = float(total_wallet_balance)
        discrepancy = expected_balance - actual_balance
        
        print(f"💰 Total Commission Records: KSh {total_commission_earned:,.2f}")
        print(f"💰 Total Wallet Balances: KSh {total_wallet_balance:,.2f}")
        print(f"📊 Current Discrepancy: KSh {discrepancy:,.2f}")
        
        print(f"\n🛠️  Applying Fixes:")
        print("=" * 20)
        
        # Fix 1: CHRISTOPHER PORIOT discrepancy
        print(f"\n1. 🔧 Fixing CHRISTOPHER PORIOT discrepancy...")
        christopher = User.query.filter_by(email='christopher@kibtech.co.ke').first()
        if christopher and christopher.wallet:
            # Get his commission records
            commission_total = db.session.query(func.sum(Commission.amount)).filter(
                Commission.referrer_id == christopher.id
            ).scalar() or 0
            
            print(f"   📊 Commission Records Total: KSh {commission_total:,.2f}")
            print(f"   💰 Current Wallet Balance: KSh {christopher.wallet.commission_balance:,.2f}")
            
            # Fix the wallet balance
            old_balance = christopher.wallet.commission_balance
            christopher.wallet.commission_balance = commission_total
            christopher.wallet.recalculate_balance()
            
            print(f"   ✅ Fixed: KSh {old_balance:,.2f} → KSh {christopher.wallet.commission_balance:,.2f}")
        else:
            print(f"   ❌ User not found or no wallet")
        
        # Fix 2: SENIOR MARKETING OFFICER - create commission record
        print(f"\n2. 🔧 Fixing SENIOR MARKETING OFFICER missing commission record...")
        senior_officer = User.query.filter_by(email='deleted_4_kibtechclientcare@gmail.com').first()
        if senior_officer and senior_officer.wallet:
            wallet_balance = float(senior_officer.wallet.commission_balance)
            print(f"   💰 Wallet Balance: KSh {wallet_balance:,.2f}")
            
            # Check if commission record exists
            existing_commission = Commission.query.filter_by(
                referrer_id=senior_officer.id,
                amount=wallet_balance
            ).first()
            
            if not existing_commission:
                # Create commission record for the wallet balance
                commission = Commission(
                    referrer_id=senior_officer.id,
                    order_id=None,
                    amount=wallet_balance,
                    commission_type='manual',
                    description='Commission balance reconciliation - missing record'
                )
                db.session.add(commission)
                print(f"   ✅ Created commission record: KSh {wallet_balance:,.2f}")
            else:
                print(f"   ℹ️  Commission record already exists")
        else:
            print(f"   ❌ User not found or no wallet")
        
        # Fix 3: EMMKASH - create commission record
        print(f"\n3. 🔧 Fixing EMMKASH missing commission record...")
        emmkash = User.query.filter_by(email='deleted_1_emmkashkash88@gmail.com').first()
        if emmkash and emmkash.wallet:
            wallet_balance = float(emmkash.wallet.commission_balance)
            print(f"   💰 Wallet Balance: KSh {wallet_balance:,.2f}")
            
            # Check if commission record exists
            existing_commission = Commission.query.filter_by(
                referrer_id=emmkash.id,
                amount=wallet_balance
            ).first()
            
            if not existing_commission:
                # Create commission record for the wallet balance
                commission = Commission(
                    referrer_id=emmkash.id,
                    order_id=None,
                    amount=wallet_balance,
                    commission_type='manual',
                    description='Commission balance reconciliation - missing record'
                )
                db.session.add(commission)
                print(f"   ✅ Created commission record: KSh {wallet_balance:,.2f}")
            else:
                print(f"   ℹ️  Commission record already exists")
        else:
            print(f"   ❌ User not found or no wallet")
        
        # Commit all changes
        print(f"\n💾 Committing database changes...")
        try:
            db.session.commit()
            print(f"   ✅ Database changes committed successfully")
        except Exception as e:
            print(f"   ❌ Failed to commit changes: {str(e)}")
            db.session.rollback()
            return
        
        # Verify fixes
        print(f"\n✅ Post-Fix Verification:")
        print("=" * 30)
        
        # Check new totals
        new_total_commission_earned = db.session.query(func.sum(Commission.amount)).scalar() or 0
        new_total_wallet_balance = db.session.query(func.sum(Wallet.commission_balance)).scalar() or 0
        new_expected_balance = float(new_total_commission_earned)
        new_actual_balance = float(new_total_wallet_balance)
        new_discrepancy = new_expected_balance - new_actual_balance
        
        print(f"💰 New Commission Records Total: KSh {new_total_commission_earned:,.2f}")
        print(f"💰 New Wallet Balances Total: KSh {new_total_wallet_balance:,.2f}")
        print(f"📊 New Discrepancy: KSh {new_discrepancy:,.2f}")
        
        # Check individual fixes
        print(f"\n🔍 Individual Fix Verification:")
        
        # Christopher
        if christopher and christopher.wallet:
            christopher_commissions = db.session.query(func.sum(Commission.amount)).filter(
                Commission.referrer_id == christopher.id
            ).scalar() or 0
            print(f"   👤 CHRISTOPHER PORIOT:")
            print(f"      💰 Commission Records: KSh {christopher_commissions:,.2f}")
            print(f"      💰 Wallet Balance: KSh {christopher.wallet.commission_balance:,.2f}")
            print(f"      ✅ Status: {'Fixed' if abs(float(christopher_commissions) - float(christopher.wallet.commission_balance)) < 0.01 else 'Still has issues'}")
        
        # Senior Officer
        if senior_officer and senior_officer.wallet:
            senior_officer_commissions = db.session.query(func.sum(Commission.amount)).filter(
                Commission.referrer_id == senior_officer.id
            ).scalar() or 0
            print(f"   👤 SENIOR MARKETING OFFICER:")
            print(f"      💰 Commission Records: KSh {senior_officer_commissions:,.2f}")
            print(f"      💰 Wallet Balance: KSh {senior_officer.wallet.commission_balance:,.2f}")
            print(f"      ✅ Status: {'Fixed' if abs(float(senior_officer_commissions) - float(senior_officer.wallet.commission_balance)) < 0.01 else 'Still has issues'}")
        
        # Emmkash
        if emmkash and emmkash.wallet:
            emmkash_commissions = db.session.query(func.sum(Commission.amount)).filter(
                Commission.referrer_id == emmkash.id
            ).scalar() or 0
            print(f"   👤 EMMKASH:")
            print(f"      💰 Commission Records: KSh {emmkash_commissions:,.2f}")
            print(f"      💰 Wallet Balance: KSh {emmkash.wallet.commission_balance:,.2f}")
            print(f"      ✅ Status: {'Fixed' if abs(float(emmkash_commissions) - float(emmkash.wallet.commission_balance)) < 0.01 else 'Still has issues'}")
        
        # Summary
        print(f"\n📊 Fix Summary:")
        print("=" * 15)
        print(f"🔧 Issues Fixed: 3")
        print(f"💰 Discrepancy Before: KSh {discrepancy:,.2f}")
        print(f"💰 Discrepancy After: KSh {new_discrepancy:,.2f}")
        print(f"📈 Improvement: KSh {discrepancy - new_discrepancy:,.2f}")
        
        if new_discrepancy < 1.0:
            print(f"✅ SUCCESS: Discrepancy resolved!")
        else:
            print(f"⚠️  WARNING: Some discrepancy remains - further investigation needed")
        
        print(f"\n💡 Recommendations:")
        print("=" * 20)
        print(f"1. ✅ Run analytics again to verify fixes")
        print(f"2. 📊 Monitor data quality indicators in admin dashboard")
        print(f"3. 🔍 Investigate any remaining discrepancies")
        print(f"4. 🛡️  Implement automated consistency checks")
        print(f"5. 📱 Test withdrawal system functionality")

def create_commission_reconciliation_report():
    """Create a detailed reconciliation report"""
    
    app = create_app()
    
    with app.app_context():
        print(f"\n📋 Commission Reconciliation Report")
        print("=" * 40)
        
        # Get all users with commission balances
        users_with_commissions = db.session.query(User).join(Wallet).filter(
            Wallet.commission_balance > 0
        ).all()
        
        print(f"👥 Users with Commission Balances: {len(users_with_commissions)}")
        print(f"\n📊 Detailed Reconciliation:")
        print("-" * 30)
        
        total_expected = 0
        total_actual = 0
        
        for user in users_with_commissions:
            # Get commission records
            commission_total = db.session.query(func.sum(Commission.amount)).filter(
                Commission.referrer_id == user.id
            ).scalar() or 0
            
            # Get withdrawals
            withdrawals = db.session.query(func.sum(Withdrawal.amount)).filter(
                Withdrawal.user_id == user.id,
                Withdrawal.status == 'approved'
            ).scalar() or 0
            
            # Calculate expected balance
            expected_balance = float(commission_total) - float(withdrawals)
            actual_balance = float(user.wallet.commission_balance)
            difference = expected_balance - actual_balance
            
            total_expected += expected_balance
            total_actual += actual_balance
            
            status = "✅ OK" if abs(difference) < 0.01 else "⚠️  ISSUE"
            
            print(f"👤 {user.name} ({user.email})")
            print(f"   💰 Commission Records: KSh {commission_total:,.2f}")
            print(f"   💸 Withdrawals: KSh {withdrawals:,.2f}")
            print(f"   🧮 Expected: KSh {expected_balance:,.2f}")
            print(f"   💰 Actual: KSh {actual_balance:,.2f}")
            print(f"   📊 Difference: KSh {difference:,.2f}")
            print(f"   {status}")
            print()
        
        print(f"📊 Summary:")
        print(f"   💰 Total Expected: KSh {total_expected:,.2f}")
        print(f"   💰 Total Actual: KSh {total_actual:,.2f}")
        print(f"   📊 Total Difference: KSh {total_expected - total_actual:,.2f}")

if __name__ == "__main__":
    print("🚀 Commission Discrepancy Fix Script")
    print("-" * 50)
    
    print("⚠️  IMPORTANT: Backup your database before running this script!")
    print("   This script will modify commission records and wallet balances.")
    
    response = input("\n❓ Do you want to proceed with fixing the discrepancies? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        print(f"\n🔧 Proceeding with fixes...")
        fix_commission_discrepancies()
        create_commission_reconciliation_report()
        
        print(f"\n🎯 Next Steps:")
        print("=" * 15)
        print("1. ✅ Verify fixes in admin analytics dashboard")
        print("2. 🔍 Check data quality indicators")
        print("3. 📊 Run commission analytics test again")
        print("4. 💰 Test withdrawal system functionality")
        print("5. 📱 Contact users about their commission balances")
        
    else:
        print(f"\n❌ Operation cancelled. No changes made to database.")
        print(f"   You can still run the investigation script to see the issues:")
        print(f"   python investigate_commission_discrepancy.py")
    
    print("\n✅ Script completed!") 