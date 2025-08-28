#!/usr/bin/env python3
"""
Fix Admin Permissions Properly
"""

import os
import sys
from app import create_app, db
from app.models import AdminUser, AdminRole

def fix_commissions_permissions():
    """Fix commissions permissions properly"""
    print("🔧 Fixing Commissions Permissions")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Find the admin user
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if not admin:
                print("❌ Admin user not found")
                return False
            
            print(f"✅ Found admin user: {admin.first_name} {admin.last_name}")
            print(f"   Email: {admin.email}")
            print(f"   Active: {admin.is_active}")
            print(f"   Super Admin: {admin.is_super_admin}")
            
            # Check role
            if admin.role:
                print(f"\n👑 Role Information:")
                print(f"   Role Name: {admin.role.name}")
                print(f"   Current Permissions: {admin.role.permissions}")
                
                # Check if commissions permissions are missing
                missing_permissions = []
                if 'view_commissions' not in admin.role.permissions:
                    missing_permissions.append('view_commissions')
                if 'manage_commissions' not in admin.role.permissions:
                    missing_permissions.append('manage_commissions')
                
                if missing_permissions:
                    print(f"\n❌ Missing permissions: {missing_permissions}")
                    print("🔧 Adding missing permissions...")
                    
                    # Add missing permissions
                    for permission in missing_permissions:
                        if permission not in admin.role.permissions:
                            admin.role.permissions.append(permission)
                            print(f"   ✅ Added {permission}")
                    
                    # Commit the changes
                    db.session.commit()
                    print("   ✅ Changes committed to database")
                    
                    # Refresh the session to get updated data
                    db.session.refresh(admin.role)
                    print("   ✅ Session refreshed")
                    
                    print(f"\n📋 Updated Permissions: {admin.role.permissions}")
                else:
                    print("✅ All required permissions are already present")
                
                # Test the permissions
                print(f"\n🔐 Testing permissions:")
                test_permissions = ['view_commissions', 'manage_commissions', 'view_dashboard']
                for permission in test_permissions:
                    has_perm = admin.has_permission(permission)
                    status = "✅" if has_perm else "❌"
                    print(f"   {status} {permission}: {has_perm}")
                
            else:
                print("❌ Admin user has no role assigned")
                return False
                
        except Exception as e:
            print(f"❌ Error fixing permissions: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

def verify_fix():
    """Verify that the fix worked"""
    print("\n🔍 Verifying Fix")
    print("=" * 30)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Get fresh data from database
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if admin and admin.role:
                print(f"✅ Role permissions: {admin.role.permissions}")
                
                # Check if permissions are in the list
                has_view = 'view_commissions' in admin.role.permissions
                has_manage = 'manage_commissions' in admin.role.permissions
                
                print(f"   view_commissions in list: {has_view}")
                print(f"   manage_commissions in list: {has_manage}")
                
                # Test has_permission method
                print(f"\n🔐 Testing has_permission method:")
                print(f"   view_commissions: {admin.has_permission('view_commissions')}")
                print(f"   manage_commissions: {admin.has_permission('manage_commissions')}")
                
                return has_view and has_manage
            else:
                print("❌ Could not verify - admin or role not found")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying fix: {str(e)}")
            return False

def main():
    """Main function"""
    print("🔧 KIBTECH Permissions Fix Tool")
    print("=" * 50)
    
    # Fix the permissions
    fix_commissions_permissions()
    
    # Verify the fix
    success = verify_fix()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Permissions fix completed successfully!")
    else:
        print("❌ Permissions fix failed!")

if __name__ == '__main__':
    main() 