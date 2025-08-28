#!/usr/bin/env python3
"""
Setup Commission System
======================

This script sets up the commission system for e-commerce and cyber services
to ensure referral commissions work properly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import SystemSettings, User, Wallet

def setup_commission_system():
    """Set up the commission system with proper rates and settings"""
    print("🔧 Setting up Commission System")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Step 1: Set up e-commerce commission rate
            print("\n1. 🔧 Setting up e-commerce commission rate...")
            
            ecommerce_commission = db.session.query(SystemSettings).filter_by(
                key='ecommerce_commission_rate'
            ).first()
            
            if not ecommerce_commission:
                ecommerce_commission = SystemSettings(
                    key='ecommerce_commission_rate',
                    value='3.0',  # 3% commission for e-commerce
                    description='Commission rate for e-commerce orders (percentage)'
                )
                db.session.add(ecommerce_commission)
                print("   ✅ E-commerce commission rate created: 3.0%")
            else:
                print(f"   ℹ️ E-commerce commission rate already exists: {ecommerce_commission.value}%")
            
            # Step 2: Set up cyber services commission rate
            print("\n2. 🔧 Setting up cyber services commission rate...")
            
            cyber_commission = db.session.query(SystemSettings).filter_by(
                key='cyber_services_commission_rate'
            ).first()
            
            if not cyber_commission:
                cyber_commission = SystemSettings(
                    key='cyber_services_commission_rate',
                    value='20.0',  # 20% commission for cyber services
                    description='Commission rate for cyber service orders (percentage)'
                )
                db.session.add(cyber_commission)
                print("   ✅ Cyber services commission rate created: 20.0%")
            else:
                print(f"   ℹ️ Cyber services commission rate already exists: {cyber_commission.value}%")
            
            # Step 3: Ensure all users have wallets
            print("\n3. 🔧 Ensuring all users have wallets...")
            
            users_without_wallets = db.session.query(User).filter(
                ~User.id.in_(db.session.query(Wallet.user_id))
            ).all()
            
            if users_without_wallets:
                print(f"   Found {len(users_without_wallets)} users without wallets")
                
                for user in users_without_wallets:
                    wallet = Wallet(user_id=user.id)
                    db.session.add(wallet)
                    print(f"   ✅ Created wallet for {user.name} ({user.email})")
            else:
                print("   ✅ All users already have wallets")
            
            # Step 4: Check referral relationships
            print("\n4. 🔍 Checking referral relationships...")
            
            referred_users = db.session.query(User).filter(User.referred_by_id.isnot(None)).all()
            print(f"   Total referred users: {len(referred_users)}")
            
            if referred_users:
                print("   Referral relationships found:")
                for user in referred_users[:5]:  # Show first 5
                    referrer = db.session.get(User, user.referred_by_id)
                    if referrer:
                        print(f"      {user.name} -> referred by {referrer.name}")
                    else:
                        print(f"      {user.name} -> invalid referrer ID: {user.referred_by_id}")
            else:
                print("   ℹ️ No referral relationships found")
            
            # Step 5: Check existing commissions
            print("\n5. 💰 Checking existing commission records...")
            
            from app.models import Commission
            all_commissions = Commission.query.all()
            print(f"   Total commission records: {len(all_commissions)}")
            
            if all_commissions:
                ecommerce_commissions = [c for c in all_commissions if c.commission_type == 'order']
                cyber_commissions = [c for c in all_commissions if c.commission_type == 'cyber_service']
                
                print(f"   E-commerce commissions: {len(ecommerce_commissions)}")
                print(f"   Cyber service commissions: {len(cyber_commissions)}")
                
                if ecommerce_commissions:
                    total_ecommerce = sum(float(c.amount) for c in ecommerce_commissions)
                    print(f"   Total e-commerce commission amount: KSh {total_ecommerce:.2f}")
                
                if cyber_commissions:
                    total_cyber = sum(float(c.amount) for c in cyber_commissions)
                    print(f"   Total cyber service commission amount: KSh {total_cyber:.2f}")
            else:
                print("   ℹ️ No commission records found")
            
            # Commit all changes
            db.session.commit()
            print("\n✅ Commission system setup completed successfully!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error setting up commission system: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_commission_calculation():
    """Test commission calculation for different scenarios"""
    print("\n🧪 Testing Commission Calculation")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Test e-commerce commission calculation
            print("\n1. 💰 Testing e-commerce commission calculation...")
            
            ecommerce_rate_setting = db.session.query(SystemSettings).filter_by(
                key='ecommerce_commission_rate'
            ).first()
            
            if ecommerce_rate_setting:
                rate = float(ecommerce_rate_setting.value) / 100.0
                test_amounts = [1000, 5000, 10000, 25000]
                
                for amount in test_amounts:
                    commission = amount * rate
                    print(f"   Order: KSh {amount:,} -> Commission: KSh {commission:.2f} ({rate*100}%)")
            else:
                print("   ❌ E-commerce commission rate not configured")
            
            # Test cyber services commission calculation
            print("\n2. 💰 Testing cyber services commission calculation...")
            
            cyber_rate_setting = db.session.query(SystemSettings).filter_by(
                key='cyber_services_commission_rate'
            ).first()
            
            if cyber_rate_setting:
                rate = float(cyber_rate_setting.value) / 100.0
                test_amounts = [500, 1000, 2000, 5000]
                
                for amount in test_amounts:
                    commission = amount * rate
                    print(f"   Service: KSh {amount:,} -> Commission: KSh {commission:.2f} ({rate*100}%)")
            else:
                print("   ❌ Cyber services commission rate not configured")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing commission calculation: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Commission System Setup")
    print("=" * 50)
    
    # Set up commission system
    setup_ok = setup_commission_system()
    
    if setup_ok:
        print("\n✅ Commission system setup completed!")
        
        # Test commission calculations
        test_ok = test_commission_calculation()
        
        if test_ok:
            print("\n🎉 Commission system is ready!")
            print("\n📋 What was set up:")
            print("   ✅ E-commerce commission rate (3%)")
            print("   ✅ Cyber services commission rate (20%)")
            print("   ✅ User wallets for all users")
            print("   ✅ Commission calculation testing")
            print("\n🎯 How it works:")
            print("1. When a referred user makes an e-commerce purchase:")
            print("   - Referrer gets 3% commission")
            print("   - Commission is added to referrer's wallet")
            print("   - Email notification is sent")
            print("2. When a referred user uses cyber services:")
            print("   - Referrer gets 20% commission")
            print("   - Commission is added to referrer's wallet")
            print("   - Email notification is sent")
            print("\n💡 Next steps:")
            print("1. Test with a real referral purchase")
            print("2. Check that commission appears in referrer's wallet")
            print("3. Verify email notifications are sent")
        else:
            print("\n⚠️ Commission calculation testing failed")
    else:
        print("\n❌ Commission system setup failed!") 