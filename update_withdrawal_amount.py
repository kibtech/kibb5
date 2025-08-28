#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import SystemSettings

def update_withdrawal_amount():
    """Update minimum withdrawal amount to KSh 10"""
    print("🔧 Updating Minimum Withdrawal Amount...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Find the min_withdrawal_amount setting
            setting = SystemSettings.query.filter_by(key='min_withdrawal_amount').first()
            
            if setting:
                print(f"Current min_withdrawal_amount: {setting.value}")
                setting.value = '10.0'
                db.session.commit()
                print("✅ Updated min_withdrawal_amount to 10.0")
            else:
                print("❌ min_withdrawal_amount setting not found")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating withdrawal amount: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🚀 Minimum Withdrawal Amount Update Tool")
    print("=" * 50)
    
    success = update_withdrawal_amount()
    
    if success:
        print("\n✅ Minimum withdrawal amount updated to KSh 10!")
        print("💡 Users can now withdraw with a minimum of KSh 10.")
    else:
        print("\n❌ Failed to update withdrawal amount. Please check the error above.") 