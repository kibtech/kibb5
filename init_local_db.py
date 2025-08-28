#!/usr/bin/env python3
"""
Initialize local SQLite database for KibTech
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, AdminUser, AdminRole, AdminPermission, Wallet, CyberService, SystemLog
from datetime import datetime

def init_local_database():
    """Initialize local SQLite database"""
    app = create_app()
    
    with app.app_context():
        print("🗄️  Initializing local SQLite database...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if admin user already exists
        admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
        if admin_user:
            print("✅ Admin user already exists")
            return
        
        # Create admin role
        admin_role = AdminRole(
            name='Super Admin',
            description='Full system access'
        )
        db.session.add(admin_role)
        db.session.flush()  # Get the ID
        
        # Create admin permissions
        permissions = [
            'view_dashboard', 'manage_products', 'manage_orders', 'manage_users',
            'manage_settings', 'view_analytics', 'manage_admins', 'manage_roles',
            'view_commissions', 'manage_commissions', 'view_users',
            'manage_cyber_services', 'view_cyber_services', 'manage_withdrawals', 'view_withdrawals'
        ]
        
        for perm_name in permissions:
            permission = AdminPermission(
                name=perm_name,
                description=f'Permission to {perm_name.replace("_", " ")}'
            )
            db.session.add(permission)
        
        db.session.flush()
        
        # Create admin user
        admin_user = AdminUser(
            username='kibtechc',
            email='kibtechc@gmail.com',
            password_hash='$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/5KQqQqG',  # password: admin123
            is_active=True,
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        
        # Create sample user
        sample_user = User(
            name='Duke Willer',
            email='kashdyke@gmail.com',
            phone='254712591937',
            password_hash='$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/5KQqQqG',  # password: admin123
            is_active=True,
            referral_code='DUKE001'
        )
        db.session.add(sample_user)
        db.session.flush()
        
        # Create wallet for sample user
        wallet = Wallet(
            user_id=sample_user.id,
            balance=100.0,
            deposited_balance=50.0,
            commission_balance=50.0
        )
        db.session.add(wallet)
        
        # Create sample cyber services
        cyber_services = [
            {
                'name': 'Website Development',
                'description': 'Professional website development services',
                'price': 50000.0,
                'category': 'Web Development',
                'is_active': True,
                'sort_order': 1
            },
            {
                'name': 'Mobile App Development',
                'description': 'iOS and Android app development',
                'price': 80000.0,
                'category': 'Mobile Development',
                'is_active': True,
                'sort_order': 2
            },
            {
                'name': 'Digital Marketing',
                'description': 'SEO, SEM, and social media marketing',
                'price': 25000.0,
                'category': 'Marketing',
                'is_active': True,
                'sort_order': 3
            }
        ]
        
        for service_data in cyber_services:
            service = CyberService(**service_data)
            db.session.add(service)
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Local database initialized successfully!")
        print("📋 Created:")
        print("   - Admin user: kibtechc@gmail.com (password: admin123)")
        print("   - Sample user: kashdyke@gmail.com (password: admin123)")
        print("   - Sample cyber services")
        print("   - Admin roles and permissions")
        print("\n🚀 You can now start the application!")

if __name__ == "__main__":
    init_local_database() 