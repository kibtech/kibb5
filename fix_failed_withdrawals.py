#!/usr/bin/env python3
"""
Fix Failed Withdrawals
This script fixes withdrawals that are marked as b2c_failed but money was actually received
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Withdrawal, User, SystemLog
from datetime import datetime

# Load environment variables
load_dotenv()

def fix_failed_withdrawals():
    """Fix withdrawals marked as b2c_failed"""
    print("🔧 Fix Failed Withdrawals")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Find all b2c_failed withdrawals
        failed_withdrawals = Withdrawal.query.filter_by(status='b2c_failed').all()
        
        if not failed_withdrawals:
            print("✅ No failed withdrawals found")
            return True
        
        print(f"📋 Found {len(failed_withdrawals)} failed withdrawals:")
        
        for withdrawal in failed_withdrawals:
            user = withdrawal.user
            print(f"   - ID: {withdrawal.id}, User: {user.name}, Amount: KSh {withdrawal.amount}, Phone: {withdrawal.phone_number}")
        
        print(f"\n🤔 Do you want to mark these as completed?")
        print(f"   (This assumes the money was actually received)")
        response = input("   Type 'yes' to continue: ").strip().lower()
        
        if response != 'yes':
            print("❌ Operation cancelled")
            return False
        
        # Mark all failed withdrawals as completed
        for withdrawal in failed_withdrawals:
            withdrawal.status = 'completed'
            withdrawal.paid_at = datetime.utcnow()
            
            # Log the manual fix
            SystemLog.create_log(
                level='INFO',
                category='wallet',
                message=f'Manually marked failed withdrawal as completed for user {withdrawal.user.name}',
                user_id=withdrawal.user_id,
                details={
                    'withdrawal_id': withdrawal.id,
                    'amount': float(withdrawal.amount),
                    'phone_number': withdrawal.phone_number,
                    'note': 'Manually fixed - money was actually received'
                }
            )
            
            print(f"✅ Fixed withdrawal ID {withdrawal.id} for {withdrawal.user.name}")
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n✅ Successfully fixed {len(failed_withdrawals)} withdrawals!")
        print(f"🎉 All failed withdrawals are now marked as completed")
        
        return True

if __name__ == "__main__":
    fix_failed_withdrawals() 