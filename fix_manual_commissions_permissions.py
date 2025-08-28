#!/usr/bin/env python3
"""
Fix Manual Commissions Permissions
This script ensures admin users have the proper permissions to access manual commissions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser, AdminRole

def fix_manual_commissions_permissions():
    """Fix permissions for manual commissions access"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Fixing Manual Commissions Permissions...")
            
            # Get all admin users
            admin_users = AdminUser.query.all()
            
            if not admin_users:
                print("❌ No admin users found!")
                return
            
            print(f"📋 Found {len(admin_users)} admin users")
            
            # Required permissions for manual commissions
            required_permissions = [
                'view_commissions',
                'manage_commissions',
                'view_users'
            ]
            
            for admin_user in admin_users:
                print(f"\n👤 Processing admin: {admin_user.email}")
                
                if not admin_user.role:
                    print(f"   ❌ No role assigned to {admin_user.email}")
                    continue
                
                print(f"   📋 Current role: {admin_user.role.name}")
                print(f"   🔑 Current permissions: {admin_user.role.permissions}")
                
                # Check if permissions list exists
                if not admin_user.role.permissions:
                    admin_user.role.permissions = []
                
                # Add missing permissions
                missing_permissions = []
                for permission in required_permissions:
                    if permission not in admin_user.role.permissions:
                        missing_permissions.append(permission)
                        admin_user.role.permissions.append(permission)
                
                if missing_permissions:
                    print(f"   ➕ Added missing permissions: {missing_permissions}")
                else:
                    print(f"   ✅ All required permissions already present")
                
                # Test permission check
                has_view_commissions = admin_user.has_permission('view_commissions')
                has_manage_commissions = admin_user.has_permission('manage_commissions')
                
                print(f"   🧪 Permission test results:")
                print(f"      - view_commissions: {has_view_commissions}")
                print(f"      - manage_commissions: {has_manage_commissions}")
            
            # Commit changes
            db.session.commit()
            print(f"\n✅ Successfully updated permissions for {len(admin_users)} admin users")
            
            # Verify changes
            print(f"\n🔍 Verifying changes...")
            for admin_user in admin_users:
                if admin_user.role:
                    has_view = admin_user.has_permission('view_commissions')
                    has_manage = admin_user.has_permission('manage_commissions')
                    print(f"   {admin_user.email}: view_commissions={has_view}, manage_commissions={has_manage}")
            
            print(f"\n🎉 Manual commissions permissions fix completed!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    fix_manual_commissions_permissions() 