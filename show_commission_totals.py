#!/usr/bin/env python3
"""
Show Commission Totals
Displays current commission totals in user wallets.
"""
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import *

def show_commission_totals():
    """Show current commission totals and user wallet balances"""
    
    app = create_app()
    
    with app.app_context():
        print("💰 Commission Totals Overview")
        print("=" * 50)
        
        # Get all wallets with commission balance
        wallets_with_commission = Wallet.query.filter(Wallet.commission_balance > 0).all()
        
        if not wallets_with_commission:
            print("❌ No users have commission balance")
            return
        
        print(f"👥 Users with Commission Balance: {len(wallets_with_commission)}")
        print()
        
        # Calculate totals
        total_commission = sum(w.commission_balance for w in wallets_with_commission)
        total_users = len(wallets_with_commission)
        
        print(f"💵 Total Commission in Wallets: KSh {total_commission:,.2f}")
        print(f"👥 Total Users with Commission: {total_users}")
        print(f"📊 Average per User: KSh {total_commission/total_users:,.2f}")
        print()
        
        # Show individual user balances
        print("👤 Individual User Commission Balances:")
        print("-" * 50)
        
        # Sort by commission balance (highest first)
        sorted_wallets = sorted(wallets_with_commission, 
                               key=lambda w: w.commission_balance, 
                               reverse=True)
        
        for i, wallet in enumerate(sorted_wallets, 1):
            user = wallet.user
            commission = wallet.commission_balance
            
            print(f"{i:2d}. {user.name or user.username or 'Unknown'}")
            print(f"    📧 {user.email}")
            print(f"    💰 Commission: KSh {commission:,.2f}")
            print(f"    🏦 Total Wallet: KSh {wallet.total_balance:,.2f}")
            print()
        
        # Show commission distribution
        print("📊 Commission Distribution:")
        print("-" * 30)
        
        ranges = [
            (0, 100, "KSh 0-100"),
            (100, 500, "KSh 100-500"),
            (500, 1000, "KSh 500-1000"),
            (1000, 5000, "KSh 1000-5000"),
            (5000, float('inf'), "KSh 5000+")
        ]
        
        for min_val, max_val, label in ranges:
            if max_val == float('inf'):
                count = len([w for w in wallets_with_commission if w.commission_balance >= min_val])
            else:
                count = len([w for w in wallets_with_commission if min_val <= w.commission_balance < max_val])
            
            if count > 0:
                percentage = (count / total_users) * 100
                print(f"   {label}: {count} users ({percentage:.1f}%)")
        
        print()
        
        # Show top earners
        print("🏆 Top 5 Commission Earners:")
        print("-" * 35)
        
        for i, wallet in enumerate(sorted_wallets[:5], 1):
            user = wallet.user
            commission = wallet.commission_balance
            print(f"{i}. {user.name or user.username or 'Unknown'}: KSh {commission:,.2f}")
        
        print()
        print("💡 To see this in Admin Portal:")
        print("   1. Go to Admin Portal → Commissions")
        print("   2. Click 'Analytics' tab")
        print("   3. View 'Total Commission Balance'")

def show_commission_records():
    """Show commission records from Commission table"""
    
    app = create_app()
    
    with app.app_context():
        print("\n📋 Commission Records Summary")
        print("=" * 40)
        
        # Get all commission records
        commissions = Commission.query.all()
        
        if not commissions:
            print("❌ No commission records found")
            return
        
        total_earned = sum(c.amount for c in commissions)
        total_withdrawn = sum(c.amount for c in commissions if c.status == 'withdrawn')
        
        print(f"💰 Total Commission Earned: KSh {total_earned:,.2f}")
        print(f"💸 Total Commission Withdrawn: KSh {total_withdrawn:,.2f}")
        print(f"💳 Remaining in System: KSh {total_earned - total_withdrawn:,.2f}")
        print()
        
        # Show by commission type
        print("📊 Commission by Type:")
        commission_types = {}
        for comm in commissions:
            comm_type = comm.commission_type or 'unknown'
            if comm_type not in commission_types:
                commission_types[comm_type] = 0
            commission_types[comm_type] += comm.amount
        
        for comm_type, amount in commission_types.items():
            print(f"   {comm_type}: KSh {amount:,.2f}")

if __name__ == "__main__":
    print("🚀 Commission Totals Display")
    print("-" * 40)
    
    show_commission_totals()
    show_commission_records()
    
    print("\n✅ Commission totals display completed!") 