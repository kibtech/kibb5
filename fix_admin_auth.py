#!/usr/bin/env python3
"""
Fix admin authentication issues
"""
import os
import re

def fix_admin_api_auth():
    """Add authentication decorators to admin API routes"""
    
    admin_api_file = 'app/admin/api.py'
    
    if not os.path.exists(admin_api_file):
        print("❌ Admin API file not found")
        return
    
    print("🔧 Fixing Admin API Authentication...")
    
    # Read the file
    with open(admin_api_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import for admin authentication
    if 'from app.admin.auth import admin_login_required' not in content:
        content = content.replace(
            'from flask import Blueprint, request, jsonify, current_app',
            'from flask import Blueprint, request, jsonify, current_app\nfrom app.admin.auth import admin_login_required'
        )
    
    # Add @admin_login_required decorator to all route functions
    # Pattern to match route definitions
    route_pattern = r'@admin_api_bp\.route\([^)]+\)\s*\n([^@\n]*\n)*def ([a-zA-Z_][a-zA-Z0-9_]*)'
    
    def add_auth_decorator(match):
        route_decorator = match.group(0)
        function_name = match.group(2)
        
        # Check if @admin_login_required is already present
        if '@admin_login_required' in route_decorator:
            return route_decorator
        
        # Add the decorator
        return f'@admin_login_required\n{route_decorator}'
    
    # Apply the fix
    new_content = re.sub(route_pattern, add_auth_decorator, content)
    
    # Write back to file
    with open(admin_api_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Admin API authentication fixed!")

def check_admin_routes():
    """Check which admin routes need authentication"""
    
    print("\n🔍 Checking Admin Routes...")
    
    # Check admin API file
    admin_api_file = 'app/admin/api.py'
    if os.path.exists(admin_api_file):
        with open(admin_api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all route definitions
        routes = re.findall(r'@admin_api_bp\.route\([^)]+\)', content)
        
        print(f"Found {len(routes)} admin API routes:")
        for route in routes:
            print(f"  - {route}")
        
        # Check if authentication is missing
        if '@admin_login_required' not in content:
            print("❌ Missing authentication decorators!")
            return True
        else:
            print("✅ Authentication decorators present")
            return False
    
    return False

if __name__ == "__main__":
    print("🔧 Admin Authentication Fix Tool")
    print("=" * 40)
    
    needs_fix = check_admin_routes()
    
    if needs_fix:
        fix_admin_api_auth()
        print("\n🔄 Checking again after fix...")
        check_admin_routes()
    else:
        print("\n✅ No fixes needed!")
    
    print("\n🎉 Admin authentication check completed!")