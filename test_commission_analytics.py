#!/usr/bin/env python3
"""
Test Commission Analytics System
Verifies the commission analytics API and data accuracy.
"""
import os
import sys
import requests
import json

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import *
from sqlalchemy import func

def test_commission_analytics_api():
    """Test the commission analytics API endpoint"""
    
    print("🧪 Testing Commission Analytics API")
    print("=" * 50)
    
    # This would normally require admin authentication
    # For now, we'll test the database queries directly
    
    app = create_app()
    
    with app.app_context():
        print("\n📊 Database-Level Commission Analytics:")
        print("=" * 40)
        
        # Total commission in all user wallets (current balance)
        total_commission_balance = db.session.query(
            func.sum(Wallet.commission_balance)
        ).scalar() or 0
        
        print(f"💰 Total Commission Balance (Current): KSh {total_commission_balance:,.2f}")
        
        # Total commission ever earned (from Commission table)
        total_commission_earned = db.session.query(
            func.sum(Commission.amount)
        ).scalar() or 0
        
        print(f"📈 Total Commission Earned (All-time): KSh {total_commission_earned:,.2f}")
        
        # Total commission withdrawn (from Withdrawal table where status = 'approved')
        total_commission_withdrawn = db.session.query(
            func.sum(Withdrawal.amount)
        ).filter(
            Withdrawal.status == 'approved'
        ).scalar() or 0
        
        print(f"💸 Total Commission Withdrawn: KSh {total_commission_withdrawn:,.2f}")
        
        # Users with commission balances
        users_with_commissions = db.session.query(User.id).join(Wallet).filter(
            Wallet.commission_balance > 0
        ).count()
        
        print(f"👥 Users with Commission Balance: {users_with_commissions}")
        
        # Total users with wallets
        total_users_with_wallets = db.session.query(User.id).join(Wallet).count()
        
        print(f"👥 Total Users with Wallets: {total_users_with_wallets}")
        
        # Average commission per user
        avg_commission = float(total_commission_balance) / users_with_commissions if users_with_commissions > 0 else 0
        
        print(f"📊 Average Commission per User: KSh {avg_commission:,.2f}")
        
        # Commission to withdrawal ratio
        commission_to_withdrawal_ratio = (float(total_commission_withdrawn) / float(total_commission_earned) * 100) if total_commission_earned > 0 else 0
        
        print(f"📈 Commission to Withdrawal Ratio: {commission_to_withdrawal_ratio:.1f}%")
        print(f"📈 Commission Retention Rate: {100 - commission_to_withdrawal_ratio:.1f}%")
        
        print(f"\n🏆 Top Commission Earners:")
        print("=" * 30)
        
        # Top commission earners (current balance)
        top_earners = db.session.query(
            User.name,
            User.email,
            Wallet.commission_balance,
            User.id
        ).join(Wallet).filter(
            Wallet.commission_balance > 0
        ).order_by(Wallet.commission_balance.desc()).limit(10).all()
        
        if top_earners:
            for i, earner in enumerate(top_earners, 1):
                print(f"  {i}. {earner.name} - KSh {earner.commission_balance:,.2f}")
                print(f"     📧 {earner.email}")
        else:
            print("  ❌ No users with commission balances found")
        
        print(f"\n📊 Commission Distribution:")
        print("=" * 30)
        
        # Commission distribution by ranges
        commission_ranges = {
            '0-100': 0,
            '100-500': 0,
            '500-1000': 0,
            '1000-5000': 0,
            '5000+': 0
        }
        
        range_query = db.session.query(Wallet.commission_balance).filter(
            Wallet.commission_balance > 0
        ).all()
        
        for wallet in range_query:
            balance = float(wallet.commission_balance)
            if balance < 100:
                commission_ranges['0-100'] += 1
            elif balance < 500:
                commission_ranges['100-500'] += 1
            elif balance < 1000:
                commission_ranges['500-1000'] += 1
            elif balance < 5000:
                commission_ranges['1000-5000'] += 1
            else:
                commission_ranges['5000+'] += 1
        
        for range_name, count in commission_ranges.items():
            percentage = (count / users_with_commissions * 100) if users_with_commissions > 0 else 0
            print(f"  KSh {range_name}: {count} users ({percentage:.1f}%)")
        
        print(f"\n💸 Withdrawal Analytics:")
        print("=" * 25)
        
        # Pending withdrawals
        pending_withdrawals = db.session.query(
            func.sum(Withdrawal.amount),
            func.count(Withdrawal.id)
        ).filter(Withdrawal.status == 'pending').first()
        
        pending_withdrawal_amount = float(pending_withdrawals[0]) if pending_withdrawals[0] else 0
        pending_withdrawal_count = pending_withdrawals[1] if pending_withdrawals[1] else 0
        
        print(f"⏳ Pending Withdrawal Amount: KSh {pending_withdrawal_amount:,.2f}")
        print(f"⏳ Pending Withdrawal Count: {pending_withdrawal_count}")
        
        # Commission liability (money owed to users)
        commission_liability = float(total_commission_balance)
        print(f"⚠️  Commission Liability: KSh {commission_liability:,.2f}")
        print(f"   (Total amount owed to users)")
        
        print(f"\n📈 Key Insights:")
        print("=" * 20)
        
        # Key business insights
        if total_commission_earned > 0:
            payout_efficiency = (float(total_commission_withdrawn) / float(total_commission_earned)) * 100
            print(f"💡 Payout Efficiency: {payout_efficiency:.1f}%")
            print(f"   ({payout_efficiency:.1f}% of earned commissions have been withdrawn)")
        
        if users_with_commissions > 0:
            print(f"💡 Active Commission Users: {users_with_commissions}/{total_users_with_wallets} ({(users_with_commissions/total_users_with_wallets*100):.1f}%)")
        
        if commission_liability > 0:
            print(f"💡 Financial Liability: KSh {commission_liability:,.2f}")
            print(f"   (Company owes this amount to users)")
        
        print(f"\n🎯 Recommendations:")
        print("=" * 20)
        
        if commission_to_withdrawal_ratio < 50:
            print("📌 Low withdrawal rate - users are accumulating commissions")
            print("   Consider marketing withdrawal features or reducing minimum amounts")
        
        if pending_withdrawal_count > 0:
            print(f"📌 {pending_withdrawal_count} pending withdrawals need admin attention")
        
        if commission_liability > 10000:  # Arbitrary threshold
            print("📌 High commission liability - monitor cash flow for payouts")
        
        highest_balance = float(top_earners[0].commission_balance) if top_earners else 0
        if highest_balance > 5000:
            print(f"📌 Top earner has KSh {highest_balance:,.2f} - consider VIP treatment")

def test_analytics_data_consistency():
    """Test data consistency across different sources"""
    
    print(f"\n🔍 Testing Data Consistency:")
    print("=" * 35)
    
    app = create_app()
    
    with app.app_context():
        # Check if commission balance matches commission records
        total_from_wallets = db.session.query(func.sum(Wallet.commission_balance)).scalar() or 0
        total_from_commissions = db.session.query(func.sum(Commission.amount)).scalar() or 0
        total_withdrawals = db.session.query(func.sum(Withdrawal.amount)).filter(
            Withdrawal.status == 'approved'
        ).scalar() or 0
        
        expected_balance = float(total_from_commissions) - float(total_withdrawals)
        actual_balance = float(total_from_wallets)
        
        print(f"💰 Commission Records Total: KSh {total_from_commissions:,.2f}")
        print(f"💸 Approved Withdrawals: KSh {total_withdrawals:,.2f}")
        print(f"🧮 Expected Wallet Balance: KSh {expected_balance:,.2f}")
        print(f"💰 Actual Wallet Balance: KSh {actual_balance:,.2f}")
        
        difference = abs(expected_balance - actual_balance)
        if difference < 1:  # Allow for small rounding differences
            print("✅ Data consistency check PASSED")
        else:
            print(f"⚠️  Data inconsistency detected: KSh {difference:,.2f} difference")
            print("   This might indicate missing commission records or incorrect calculations")

if __name__ == "__main__":
    print("🚀 Commission Analytics Test Suite")
    print("-" * 50)
    
    test_commission_analytics_api()
    test_analytics_data_consistency()
    
    print(f"\n📝 API Testing Notes:")
    print("=" * 25)
    print("To test the full API endpoint:")
    print("1. Authenticate as admin")
    print("2. GET /admin/commissions/analytics")
    print("3. Check response matches database calculations")
    print("4. Verify frontend displays data correctly")
    
    print("\n✅ Commission Analytics Test completed!")