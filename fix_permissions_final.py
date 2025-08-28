#!/usr/bin/env python3
"""
Fix Admin Permissions - Final Version
"""

import os
import sys
from app import create_app, db
from app.models import AdminUser, AdminRole
from sqlalchemy import inspect

def fix_commissions_permissions():
    """Fix commissions permissions properly"""
    print("🔧 Fixing Commissions Permissions - Final Version")
    print("=" * 60)
    
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
                    
                    # Create a new list with the missing permissions
                    current_permissions = admin.role.permissions or []
                    updated_permissions = current_permissions + missing_permissions
                    
                    print(f"   Current: {current_permissions}")
                    print(f"   Updated: {updated_permissions}")
                    
                    # Update the permissions field
                    admin.role.permissions = updated_permissions
                    
                    # Explicitly mark the field as modified
                    from sqlalchemy.orm.attributes import flag_modified
                    flag_modified(admin.role, "permissions")
                    
                    print("   ✅ Updated permissions field")
                    print("   ✅ Flagged field as modified")
                    
                    # Commit the changes
                    db.session.commit()
                    print("   ✅ Changes committed to database")
                    
                    # Verify the changes
                    db.session.refresh(admin.role)
                    print(f"   ✅ Session refreshed")
                    print(f"   📋 Final Permissions: {admin.role.permissions}")
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

def test_commissions_endpoint():
    """Test the commissions endpoint after fix"""
    print("\n🧪 Testing Commissions Endpoint")
    print("=" * 35)
    
    import requests
    import json
    
    try:
        # Login to get token
        login_data = {
            'email': 'kibtechc@gmail.com',
            'password': 'Kibtechceo@2018'
        }
        
        login_response = requests.post(
            'http://localhost:5000/admin/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['token']
            print("✅ Login successful")
            
            # Test commissions endpoint
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            commissions_response = requests.get(
                'http://localhost:5000/admin/commissions/manual',
                headers=headers
            )
            
            print(f"Commissions Status: {commissions_response.status_code}")
            if commissions_response.status_code == 200:
                print("✅ Commissions endpoint working!")
                return True
            else:
                print(f"❌ Commissions endpoint failed: {commissions_response.text}")
                return False
        else:
            print(f"❌ Login failed: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing endpoint: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔧 KIBTECH Permissions Fix Tool - Final Version")
    print("=" * 60)
    
    # Fix the permissions
    fix_commissions_permissions()
    
    # Verify the fix
    success = verify_fix()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Permissions fix completed successfully!")
        
        # Test the endpoint
        endpoint_success = test_commissions_endpoint()
        if endpoint_success:
            print("🎉 Everything is working! You can now access commissions in the admin portal.")
        else:
            print("⚠️  Permissions fixed but endpoint test failed. Check if backend is running.")
    else:
        print("\n" + "=" * 60)
        print("❌ Permissions fix failed!")

if __name__ == '__main__':
    main() 