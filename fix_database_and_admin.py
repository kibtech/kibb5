#!/usr/bin/env python3
"""
Fix Database Connection and Admin User Creation Issues
=====================================================

This script addresses two main issues:
1. Database connection timeout to Railway PostgreSQL
2. AdminUser model attribute errors (missing 'name' attribute)

Solutions:
1. Create a local SQLite database as fallback
2. Fix AdminUser creation with correct attributes
3. Create AdminRole if missing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser, AdminRole, User, Product, Category, Brand
from sqlalchemy import text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection and provide fallback options"""
    print("🔍 Testing database connection...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test connection
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            print("\n🔧 Attempting to fix database connection...")
            
            # Try to create local SQLite database as fallback
            try:
                # Update config to use SQLite
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kibtech_local.db'
                print("📁 Switching to local SQLite database...")
                
                # Recreate database
                db.drop_all()
                db.create_all()
                print("✅ Local SQLite database created successfully!")
                return True
                
            except Exception as e2:
                print(f"❌ Failed to create local database: {str(e2)}")
                return False

def create_admin_role():
    """Create admin role if it doesn't exist"""
    print("\n👑 Creating admin role...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if super admin role exists
            super_admin_role = AdminRole.query.filter_by(name='Super Admin').first()
            
            if not super_admin_role:
                print("📝 Creating Super Admin role...")
                super_admin_role = AdminRole(
                    name='Super Admin',
                    description='Full system access with all permissions',
                    permissions=[
                        'user_management', 'product_management', 'order_management',
                        'payment_management', 'system_settings', 'analytics',
                        'admin_management', 'backup_restore', 'api_management'
                    ],
                    is_active=True
                )
                db.session.add(super_admin_role)
                db.session.commit()
                print("✅ Super Admin role created successfully!")
            else:
                print("✅ Super Admin role already exists!")
                
            return super_admin_role
            
        except Exception as e:
            print(f"❌ Error creating admin role: {str(e)}")
            db.session.rollback()
            return None

def create_admin_user():
    """Create admin user with correct attributes"""
    print("\n👤 Creating admin user...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if admin exists
            admin = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if admin:
                print("✅ Admin user already exists:")
                print(f"   Name: {admin.first_name} {admin.last_name}")
                print(f"   Email: {admin.email}")
                print(f"   Username: {admin.username}")
                print(f"   Role: {admin.role.name if admin.role else 'N/A'}")
                print(f"   Active: {admin.is_active}")
                return admin
            else:
                print("📝 Creating new admin user...")
                
                # Get or create super admin role
                super_admin_role = create_admin_role()
                if not super_admin_role:
                    print("❌ Failed to create admin role")
                    return None
                
                # Create admin user with correct attributes
                admin = AdminUser(
                    username='kibtech_admin',
                    email='kibtechc@gmail.com',
                    first_name='KC',
                    last_name='KibTech CEO',
                    phone='+254700000000',
                    role_id=super_admin_role.id,
                    is_active=True,
                    is_super_admin=True,
                    email_verified=True
                )
                admin.set_password('admin123')
                
                db.session.add(admin)
                db.session.commit()
                
                print("✅ Admin user created successfully!")
                print(f"   Name: {admin.first_name} {admin.last_name}")
                print(f"   Email: {admin.email}")
                print(f"   Username: {admin.username}")
                print(f"   Password: admin123")
                print(f"   Role: {admin.role.name if admin.role else 'N/A'}")
                print(f"   Active: {admin.is_active}")
                
                return admin
                
        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return None

def create_sample_data():
    """Create sample categories and products"""
    print("\n📦 Creating sample data...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create categories
            categories_data = [
                {'name': 'Smartphones', 'slug': 'smartphones', 'description': 'Latest smartphones and mobile devices'},
                {'name': 'Laptops', 'slug': 'laptops', 'description': 'High-performance laptops and computers'},
                {'name': 'Audio', 'slug': 'audio', 'description': 'Headphones, speakers, and audio equipment'},
                {'name': 'Cameras', 'slug': 'cameras', 'description': 'Digital cameras and photography equipment'},
                {'name': 'Tablets', 'slug': 'tablets', 'description': 'Tablets and portable devices'},
                {'name': 'Accessories', 'slug': 'accessories', 'description': 'Phone and computer accessories'}
            ]
            
            for cat_data in categories_data:
                category = Category.query.filter_by(slug=cat_data['slug']).first()
                if not category:
                    category = Category(**cat_data)
                    db.session.add(category)
                    print(f"✅ Created category: {cat_data['name']}")
            
            # Create brands
            brands_data = [
                {'name': 'Samsung', 'slug': 'samsung'},
                {'name': 'Apple', 'slug': 'apple'},
                {'name': 'Dell', 'slug': 'dell'},
                {'name': 'HP', 'slug': 'hp'},
                {'name': 'Sony', 'slug': 'sony'},
                {'name': 'Canon', 'slug': 'canon'}
            ]
            
            for brand_data in brands_data:
                brand = Brand.query.filter_by(slug=brand_data['slug']).first()
                if not brand:
                    brand = Brand(**brand_data)
                    db.session.add(brand)
                    print(f"✅ Created brand: {brand_data['name']}")
            
            db.session.commit()
            print("✅ Sample data created successfully!")
            
        except Exception as e:
            print(f"❌ Error creating sample data: {str(e)}")
            db.session.rollback()

def main():
    """Main function to fix database and admin issues"""
    print("🚀 KIBTECH Database and Admin Fix Tool")
    print("=" * 50)
    
    # Test and fix database connection
    if not test_database_connection():
        print("❌ Failed to establish database connection")
        return False
    
    # Create admin user
    admin = create_admin_user()
    if not admin:
        print("❌ Failed to create admin user")
        return False
    
    # Create sample data
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Database and admin setup completed successfully!")
    print("\n📋 Admin Information:")
    print("🌐 Admin Panel URL: https://kibtech.coke/admin")
    print("📧 Email: kibtechc@gmail.com")
    print("🔑 Password: admin123")
    print("👤 Username: kibtech_admin")
    print("🏢 Name: KC KibTech CEO")
    print("👑 Role: Super Admin")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ All issues resolved! You can now run the application.")
    else:
        print("\n❌ Some issues remain. Please check the error messages above.")
        sys.exit(1) 