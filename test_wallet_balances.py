#!/usr/bin/env python3
"""
Test Wallet Balances
This script tests wallet balances to ensure they're being displayed correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Wallet, Commission
from decimal import Decimal

def test_wallet_balances():
    """Test wallet balances display"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🧪 Testing Wallet Balances...")
            
            # Get all users
            users = User.query.all()
            print(f"📋 Found {len(users)} users")
            
            for user in users:
                print(f"\n👤 User: {user.name} ({user.email})")
                
                if user.wallet:
                    print(f"   💰 Total Balance: KSh {float(user.wallet.balance):,.2f}")
                    print(f"   💳 Commission Balance: KSh {float(user.wallet.commission_balance):,.2f}")
                    print(f"   💵 Deposited Balance: KSh {float(user.wallet.deposited_balance):,.2f}")
                else:
                    print("   ❌ No wallet found")
                
                # Check commission history
                commissions = Commission.query.filter_by(referrer_id=user.id).all()
                total_commissions = sum(float(c.amount) for c in commissions)
                print(f"   📊 Total Commissions Earned: KSh {total_commissions:,.2f}")
                print(f"   📈 Commission Count: {len(commissions)}")
            
            # Test the new endpoint
            print(f"\n🌐 Testing new endpoint...")
            from app.admin.commissions import get_users_with_wallets
            
            # Simulate the endpoint call
            with app.test_request_context('/admin/commissions/users-with-wallets'):
                response = get_users_with_wallets()
                if hasattr(response, 'json'):
                    data = response.json
                    print(f"✅ Endpoint working: {len(data.get('users', []))} users returned")
                    
                    # Show first user as example
                    if data.get('users'):
                        first_user = data['users'][0]
                        print(f"📋 Example user data:")
                        print(f"   Name: {first_user['name']}")
                        print(f"   Wallet Balance: KSh {first_user['wallet']['balance']:,.2f}")
                        print(f"   Commission Balance: KSh {first_user['wallet']['commission_balance']:,.2f}")
                else:
                    print("❌ Endpoint not working properly")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_wallet_balances() 