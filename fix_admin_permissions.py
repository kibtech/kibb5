#!/usr/bin/env python3
"""
Fix Admin Permissions Script
This script ensures admin users have proper permissions to access all admin features.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser, AdminRole

def fix_admin_permissions():
    """Fix admin user permissions and roles"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Fixing admin permissions...")
            
            # Check if admin roles exist
            admin_role = db.session.query(AdminRole).filter_by(name='Administrator').first()
            
            if not admin_role:
                print("📝 Creating Administrator role...")
                admin_role = AdminRole(
                    name='Administrator',
                    description='Full system administrator with all permissions',
                    permissions=[
                        'manage_users',
                        'manage_products', 
                        'manage_orders',
                        'manage_cyber_services',
                        'manage_cyber_service_orders',
                        'manage_inventory',
                        'manage_categories',
                        'manage_brands',
                        'manage_coupons',
                        'manage_shipping',
                        'manage_taxes',
                        'manage_commissions',
                        'manage_withdrawals',
                        'manage_system_settings',
                        'view_analytics',
                        'view_reports',
                        'manage_admin_users',
                        'manage_admin_roles',
                        'view_logs',
                        'manage_backups',
                        'manage_api_keys',
                        'manage_email_templates',
                        'manage_feature_flags',
                        'manage_maintenance_mode'
                    ],
                    is_active=True
                )
                db.session.add(admin_role)
                db.session.commit()
                print("✅ Administrator role created successfully")
            else:
                print("✅ Administrator role already exists")
                # Update permissions to ensure they're current
                current_permissions = admin_role.permissions or []
                required_permissions = [
                    'manage_users',
                    'manage_products', 
                    'manage_orders',
                    'manage_cyber_services',
                    'manage_cyber_service_orders',
                    'manage_inventory',
                    'manage_categories',
                    'manage_brands',
                    'manage_coupons',
                    'manage_shipping',
                    'manage_taxes',
                    'manage_commissions',
                    'manage_withdrawals',
                    'manage_system_settings',
                    'view_analytics',
                    'view_reports',
                    'manage_admin_users',
                    'manage_admin_roles',
                    'view_logs',
                    'manage_backups',
                    'manage_api_keys',
                    'manage_email_templates',
                    'manage_feature_flags',
                    'manage_maintenance_mode'
                ]
                
                # Add any missing permissions
                updated = False
                for permission in required_permissions:
                    if permission not in current_permissions:
                        current_permissions.append(permission)
                        updated = True
                
                if updated:
                    admin_role.permissions = current_permissions
                    db.session.commit()
                    print("✅ Administrator role permissions updated")
                else:
                    print("✅ Administrator role permissions are up to date")
            
            # Check if admin users exist
            admin_users = db.session.query(AdminUser).all()
            
            if not admin_users:
                print("❌ No admin users found! Please create an admin user first.")
                print("💡 You can use: python create_admin_user.py")
                return False
            
            print(f"👥 Found {len(admin_users)} admin user(s)")
            
            # Ensure all admin users have the Administrator role
            for admin_user in admin_users:
                if not admin_user.role or admin_user.role.name != 'Administrator':
                    print(f"🔄 Updating {admin_user.email} to Administrator role...")
                    admin_user.role = admin_role
                    admin_user.is_super_admin = True
                    db.session.commit()
                    print(f"✅ {admin_user.email} updated successfully")
                else:
                    print(f"✅ {admin_user.email} already has Administrator role")
            
            print("\n🎉 Admin permissions fixed successfully!")
            print("\n📋 Summary:")
            print(f"   • Administrator role: {'✅' if admin_role else '❌'}")
            print(f"   • Admin users: {len(admin_users)}")
            print(f"   • Permissions: {len(admin_role.permissions) if admin_role else 0}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error fixing admin permissions: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = fix_admin_permissions()
    if success:
        print("\n🚀 You should now be able to access all admin features!")
        print("💡 Try logging into the admin portal again.")
    else:
        print("\n❌ Failed to fix admin permissions. Check the error above.")
        sys.exit(1) 