#!/usr/bin/env python3
"""
Setup script to fix manual commissions issue
This script will:
1. Update the Commission model schema
2. Run database migrations
3. Test manual commission creation
"""

from app import create_app, db
from app.models import User, Commission, Wallet, AdminUser
from decimal import Decimal
import logging

def setup_manual_commissions():
    """Setup manual commissions functionality"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Setting up manual commissions...")
            
            # Step 1: Run database migration
            print("\n1. Running database migration...")
            from fix_commission_schema import migrate_commission_schema
            migrate_commission_schema()
            
            # Step 2: Test manual commission creation
            print("\n2. Testing manual commission creation...")
            
            # Find a user with a wallet
            user_with_wallet = db.session.query(User).join(Wallet).first()
            
            if not user_with_wallet:
                print("❌ No users with wallets found. Please create a user and wallet first.")
                return
            
            print(f"✅ Found user: {user_with_wallet.name} (ID: {user_with_wallet.id})")
            
            # Test creating a manual commission
            test_commission = Commission(
                referrer_id=user_with_wallet.id,
                order_id=None,  # No order for manual commission
                amount=Decimal('50.00'),
                commission_type='manual',
                description='Test manual commission'
            )
            
            db.session.add(test_commission)
            db.session.commit()
            
            print(f"✅ Successfully created test manual commission (ID: {test_commission.id})")
            
            # Update user's wallet
            user_with_wallet.wallet.add_commission(Decimal('50.00'))
            print(f"✅ Updated wallet balance: KSh {user_with_wallet.wallet.commission_balance}")
            
            # Clean up test commission
            db.session.delete(test_commission)
            user_with_wallet.wallet.add_commission(Decimal('-50.00'))  # Remove the test amount
            db.session.commit()
            
            print("✅ Test commission cleaned up")
            
            print("\n🎉 Manual commissions setup completed successfully!")
            print("\nYou can now:")
            print("- Add manual commissions through the admin panel")
            print("- Remove manual commissions through the admin panel")
            print("- View manual commissions in the wallet page")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during setup: {str(e)}")
            raise

if __name__ == "__main__":
    setup_manual_commissions() 