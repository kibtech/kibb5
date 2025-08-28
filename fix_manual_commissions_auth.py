#!/usr/bin/env python3
"""
Fix Manual Commissions Authentication
This script provides a comprehensive fix for the manual commissions authentication issue.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser, User, Commission, Wallet
from decimal import Decimal
from datetime import datetime

def fix_manual_commissions_auth():
    """Comprehensive fix for manual commissions authentication"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Comprehensive Manual Commissions Authentication Fix...")
            
            # 1. Verify admin user exists and has proper permissions
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            if not admin_user:
                print("❌ Admin user not found!")
                return
            
            print(f"✅ Admin user found: {admin_user.email}")
            print(f"✅ Is active: {admin_user.is_active}")
            print(f"✅ Is super admin: {admin_user.is_super_admin}")
            
            # 2. Ensure admin has proper role and permissions
            if not admin_user.role:
                print("❌ Admin user has no role assigned!")
                return
            
            print(f"✅ Admin role: {admin_user.role.name}")
            
            # Required permissions for manual commissions
            required_permissions = [
                'view_commissions',
                'manage_commissions',
                'view_users'
            ]
            
            # Add missing permissions
            missing_permissions = []
            for permission in required_permissions:
                if permission not in admin_user.role.permissions:
                    missing_permissions.append(permission)
                    admin_user.role.permissions.append(permission)
            
            if missing_permissions:
                print(f"➕ Added missing permissions: {missing_permissions}")
            else:
                print(f"✅ All required permissions present")
            
            # 3. Test permission checks
            print(f"\n🧪 Testing permission checks:")
            for permission in required_permissions:
                has_perm = admin_user.has_permission(permission)
                print(f"   {permission}: {has_perm}")
            
            # 4. Ensure there are users with wallets for testing
            users_with_wallets = User.query.join(Wallet).all()
            print(f"\n👥 Users with wallets: {len(users_with_wallets)}")
            
            if not users_with_wallets:
                print("⚠️  No users with wallets found. Creating a test user...")
                
                # Create a test user with wallet
                test_user = User(
                    name='Test User',
                    email='test@example.com',
                    phone='1234567890',
                    password_hash='dummy_hash'
                )
                test_user.generate_referral_code()
                db.session.add(test_user)
                db.session.flush()  # Get the user ID
                
                # Create wallet for test user
                wallet = Wallet(user_id=test_user.id)
                db.session.add(wallet)
                
                print(f"✅ Created test user: {test_user.email}")
            
            # 5. Check existing manual commissions
            manual_commissions = Commission.query.all()
            print(f"💰 Existing commissions: {len(manual_commissions)}")
            
            # 6. Commit all changes
            db.session.commit()
            print(f"\n✅ All changes committed successfully")
            
            # 7. Final verification
            print(f"\n🔍 Final verification:")
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            print(f"   Admin permissions: {admin_user.role.permissions}")
            print(f"   Has view_commissions: {admin_user.has_permission('view_commissions')}")
            print(f"   Has manage_commissions: {admin_user.has_permission('manage_commissions')}")
            
            print(f"\n🎉 Manual commissions authentication fix completed!")
            print(f"\n📋 Next steps:")
            print(f"   1. Restart your backend server")
            print(f"   2. Clear browser cache and localStorage")
            print(f"   3. Login to admin panel again")
            print(f"   4. Navigate to Manual Commissions page")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    fix_manual_commissions_auth() 