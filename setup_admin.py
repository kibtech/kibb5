#!/usr/bin/env python3
"""
Setup script for KibTech Admin Portal
Creates default admin roles, super admin user, and system settings
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminRole, AdminUser, SystemSettings
from datetime import datetime

def setup_admin_system():
    """Initialize the admin system with default data"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Setting up KibTech Admin Portal...")
        
        # Create default admin roles
        print("📋 Creating default admin roles...")
        
        # Super Admin role
        super_admin_role = AdminRole.query.filter_by(name='Super Admin').first()
        if not super_admin_role:
            super_admin_role = AdminRole(
                name='Super Admin',
                description='Full access to all system features',
                permissions=[
                    'view_dashboard',
                    'manage_products',
                    'manage_orders',
                    'manage_users',
                    'manage_settings',
                    'view_analytics',
                    'manage_admins',
                    'manage_roles'
                ],
                is_active=True
            )
            db.session.add(super_admin_role)
            print("✅ Created Super Admin role")
        else:
            print("ℹ️  Super Admin role already exists")
        
        # Manager role
        manager_role = AdminRole.query.filter_by(name='Manager').first()
        if not manager_role:
            manager_role = AdminRole(
                name='Manager',
                description='Can manage products, orders, and users',
                permissions=[
                    'view_dashboard',
                    'manage_products',
                    'manage_orders',
                    'manage_users',
                    'view_analytics'
                ],
                is_active=True
            )
            db.session.add(manager_role)
            print("✅ Created Manager role")
        else:
            print("ℹ️  Manager role already exists")
        
        # Support role
        support_role = AdminRole.query.filter_by(name='Support').first()
        if not support_role:
            support_role = AdminRole(
                name='Support',
                description='Can view orders and manage basic operations',
                permissions=[
                    'view_dashboard',
                    'manage_orders',
                    'view_analytics'
                ],
                is_active=True
            )
            db.session.add(support_role)
            print("✅ Created Support role")
        else:
            print("ℹ️  Support role already exists")
        
        db.session.commit()
        
        # Create default super admin user
        print("👤 Creating default super admin user...")
        admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
        if not admin_user:
            # Get the super admin role
            super_admin_role = AdminRole.query.filter_by(name='Super Admin').first()
            if not super_admin_role:
                print("❌ Super Admin role not found!")
                return
            
            admin_user = AdminUser(
                username='kibtech_admin',
                email='kibtechc@gmail.com',
                first_name='KibTech',
                last_name='CEO',
                role_id=super_admin_role.id,
                is_active=True,
                is_super_admin=True
            )
            admin_user.set_password('Kibtechceo@2018')
            db.session.add(admin_user)
            print("✅ Created admin user with specified credentials")
        else:
            # Update existing user's password
            admin_user.set_password('Kibtechceo@2018')
            print("✅ Updated existing admin user password")
        
        db.session.commit()
        
        # Create default system settings
        print("⚙️  Creating default system settings...")
        
        default_settings = [
            {
                'key': 'store_name',
                'value': 'KibTech Online Services',
                'description': 'Store name displayed to customers',
                'category': 'general',
                'is_public': True
            },
            {
                'key': 'store_email',
                'value': 'kibtechc@gmail.com',
                'description': 'Primary store email address',
                'category': 'general',
                'is_public': True
            },
            {
                'key': 'store_phone',
                'value': '+254700000000',
                'description': 'Store contact phone number',
                'category': 'general',
                'is_public': True
            },
            {
                'key': 'commission_rate',
                'value': '10.0',
                'description': 'Default commission rate for referrals (%)',
                'category': 'financial',
                'is_public': False
            },
            {
                'key': 'mpesa_business_number',
                'value': '123456789',
                'description': 'M-Pesa business number for payments',
                'category': 'payment',
                'is_public': False
            },
            {
                'key': 'min_withdrawal_amount',
                'value': '10.0',
                'description': 'Minimum withdrawal amount',
                'category': 'financial',
                'is_public': True
            },
            {
                'key': 'tax_rate',
                'value': '16.0',
                'description': 'Default tax rate (%)',
                'category': 'financial',
                'is_public': False
            },
            {
                'key': 'shipping_cost',
                'value': '500.0',
                'description': 'Default shipping cost',
                'category': 'shipping',
                'is_public': True
            },
            {
                'key': 'free_shipping_threshold',
                'value': '5000.0',
                'description': 'Order amount for free shipping',
                'category': 'shipping',
                'is_public': True
            },
            {
                'key': 'low_stock_threshold',
                'value': '10',
                'description': 'Stock level to trigger low stock alerts',
                'category': 'inventory',
                'is_public': False
            }
        ]
        
        for setting_data in default_settings:
            existing_setting = SystemSettings.query.filter_by(key=setting_data['key']).first()
            if not existing_setting:
                setting = SystemSettings(**setting_data)
                db.session.add(setting)
                print(f"✅ Created setting: {setting_data['key']}")
            else:
                print(f"ℹ️  Setting already exists: {setting_data['key']}")
        
        db.session.commit()
        
        print("\n🎉 KibTech Admin Portal setup completed successfully!")
        print("\n📋 Admin credentials:")
        print("   Email: kibtechc@gmail.com")
        print("   Password: Kibtechceo@2018")
        print("\n🔗 Access the admin portal at: https://kibtech.coke/admin/login")
        print("\n⚠️  IMPORTANT: Keep your credentials secure!")

if __name__ == '__main__':
    setup_admin_system() 