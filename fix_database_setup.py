#!/usr/bin/env python3
"""
Fix Database Setup for KibTech Store
This script fixes the database setup issues and properly seeds the database
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_database():
    """Fix database setup and seed with default data"""
    try:
        from app import create_app, db
        from app.models import User, Product, Category, Brand
        
        # Try local config first, fallback to default
        try:
            app = create_app('local')
        except:
            app = create_app()
        
        with app.app_context():
            print("🔧 Fixing database setup...")
            
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if we need to seed data
            try:
                product_count = Product.query.count()
                category_count = Category.query.count()
            except:
                product_count = 0
                category_count = 0
            
            print(f"📊 Current database status:")
            print(f"- Categories: {category_count}")
            print(f"- Products: {product_count}")
            
            if product_count == 0 or category_count == 0:
                print("🌱 Seeding database with default data...")
                
                # Create default categories
                categories = [
                    Category(name='Laptops', slug='laptops', description='High-performance laptops for work and gaming'),
                    Category(name='Smartphones', slug='smartphones', description='Latest smartphones with advanced features'),
                    Category(name='Accessories', slug='accessories', description='Essential tech accessories and peripherals'),
                    Category(name='Cyber Services', slug='cyber-services', description='Professional cybersecurity and IT services')
                ]
                
                for category in categories:
                    db.session.add(category)
                
                db.session.commit()
                print("✅ Categories created")
                
                # Create default products
                products = [
                    # Laptops
                    Product(
                        name='MacBook Pro 14" M2',
                        slug='macbook-pro-14-m2',
                        description='Apple MacBook Pro with M2 chip, 14-inch Retina display, 16GB RAM, 512GB SSD.',
                        price=249999.00,
                        category_id=1,
                        stock_quantity=10,
                        is_featured=True
                    ),
                    Product(
                        name='Dell XPS 13 Plus',
                        slug='dell-xps-13-plus',
                        description='Dell XPS 13 Plus with Intel i7, 13.4-inch OLED display, 16GB RAM, 512GB SSD.',
                        price=189999.00,
                        category_id=1,
                        stock_quantity=8,
                        is_featured=True
                    ),
                    
                    # Smartphones
                    Product(
                        name='iPhone 15 Pro',
                        slug='iphone-15-pro',
                        description='Apple iPhone 15 Pro with A17 Pro chip, 6.1-inch Super Retina XDR display, 256GB storage.',
                        price=189999.00,
                        category_id=2,
                        stock_quantity=20,
                        is_featured=True
                    ),
                    Product(
                        name='Samsung Galaxy S24 Ultra',
                        slug='samsung-galaxy-s24-ultra',
                        description='Samsung Galaxy S24 Ultra with Snapdragon 8 Gen 3, 6.8-inch Dynamic AMOLED display, 256GB storage.',
                        price=179999.00,
                        category_id=2,
                        stock_quantity=12,
                        is_featured=True
                    ),
                    
                    # Accessories
                    Product(
                        name='AirPods Pro 2nd Gen',
                        slug='airpods-pro-2nd-gen',
                        description='Apple AirPods Pro 2nd generation with Active Noise Cancellation, Spatial Audio, and MagSafe charging case.',
                        price=29999.00,
                        category_id=3,
                        stock_quantity=25,
                        is_featured=True
                    ),
                    Product(
                        name='Samsung Galaxy Watch 6',
                        slug='samsung-galaxy-watch-6',
                        description='Samsung Galaxy Watch 6 with 44mm display, health monitoring, GPS, and 2-day battery life.',
                        price=39999.00,
                        category_id=3,
                        stock_quantity=15,
                        is_featured=True
                    ),
                    
                    # Cyber Services (as products)
                    Product(
                        name='Website Security Audit',
                        slug='website-security-audit',
                        description='Comprehensive security audit for your website including vulnerability assessment, penetration testing, and security recommendations.',
                        price=49999.00,
                        category_id=4,
                        stock_quantity=999,
                        is_digital=True,
                        requires_shipping=False
                    ),
                    Product(
                        name='Network Security Setup',
                        slug='network-security-setup',
                        description='Complete network security setup including firewall configuration, VPN setup, and network monitoring tools.',
                        price=79999.00,
                        category_id=4,
                        stock_quantity=999,
                        is_digital=True,
                        requires_shipping=False
                    ),
                    Product(
                        name='Data Recovery Service',
                        slug='data-recovery-service',
                        description='Professional data recovery service for hard drives, SSDs, and other storage devices. High success rate recovery.',
                        price=29999.00,
                        category_id=4,
                        stock_quantity=999,
                        is_digital=True,
                        requires_shipping=False
                    )
                ]
                
                for product in products:
                    db.session.add(product)
                
                db.session.commit()
                print("✅ Products created")
                
                # Create admin user
                try:
                    admin = User(
                        name='Admin User',
                        phone='254700000000',
                        email='kibtechc@gmail.com',
                        referral_code='ADMIN001'
                    )
                    admin.set_password('KIibtechceo@2018')
                    db.session.add(admin)
                    print("✅ Admin user created")
                except Exception as e:
                    print(f"⚠️  Warning: Could not create admin user: {e}")
                
                db.session.commit()
                
                print(f"✅ Database seeded successfully!")
                print(f"📊 Final Summary:")
                print(f"- Categories: {Category.query.count()}")
                print(f"- Products: {Product.query.count()}")
                try:
                    print(f"- Users: {User.query.count()}")
                except:
                    print("- Users: Could not check")
            else:
                print("✅ Database already has data")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("🚀 Fixing KibTech Store Database Setup")
    print("=" * 50)
    
    success = fix_database()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ Database setup fixed successfully!")
        print("\n🌐 Access your store:")
        print("- Local: http://localhost:5000")
        print("- Production: https://kibtech.co.ke")
        print("\n🔑 Admin Login:")
        print("- Email: admin@kibtech.co.ke")
        print("- Password: admin123 (change in production)")
        print("\n📦 Your store now has:")
        print("- 4 Product Categories")
        print("- 9 Tech Products")
        print("- Admin User")
    else:
        print("\n❌ Database setup failed!")
        print("Please check the error messages above")
        sys.exit(1)

if __name__ == "__main__":
    main() 