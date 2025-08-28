#!/usr/bin/env python3
"""
Heroku Database Setup for KibTech Store
This script handles database initialization and seeding for both local and Heroku environments
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_heroku_database():
    """Setup database for Heroku deployment"""
    try:
        from app import create_app, db
        from app.models import User, Product, Category, CommissionRate, Settings
        
        app = create_app('heroku')
        
        with app.app_context():
            print("🚀 Setting up Heroku database...")
            
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if we need to seed data
            product_count = Product.query.count()
            category_count = Category.query.count()
            
            if product_count == 0 or category_count == 0:
                print("🌱 Database is empty, seeding with default data...")
                
                # Create default categories
                categories = [
                    Category(name='Laptops', description='High-performance laptops for work and gaming'),
                    Category(name='Smartphones', description='Latest smartphones with advanced features'),
                    Category(name='Accessories', description='Essential tech accessories and peripherals'),
                    Category(name='Cyber Services', description='Professional cybersecurity and IT services')
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
                        description='Apple MacBook Pro with M2 chip, 14-inch Retina display, 16GB RAM, 512GB SSD.',
                        price=249999.00,
                        category_id=1,
                        stock=10,
                        features='M2 Chip, 14" Retina Display, 16GB RAM, 512GB SSD, macOS'
                    ),
                    Product(
                        name='Dell XPS 13 Plus',
                        description='Dell XPS 13 Plus with Intel i7, 13.4-inch OLED display, 16GB RAM, 512GB SSD.',
                        price=189999.00,
                        category_id=1,
                        stock=8,
                        features='Intel i7, 13.4" OLED, 16GB RAM, 512GB SSD, Windows 11'
                    ),
                    
                    # Smartphones
                    Product(
                        name='iPhone 15 Pro',
                        description='Apple iPhone 15 Pro with A17 Pro chip, 6.1-inch Super Retina XDR display, 256GB storage.',
                        price=189999.00,
                        category_id=2,
                        stock=20,
                        features='A17 Pro Chip, 6.1" Super Retina XDR, 256GB, iOS 17'
                    ),
                    Product(
                        name='Samsung Galaxy S24 Ultra',
                        description='Samsung Galaxy S24 Ultra with Snapdragon 8 Gen 3, 6.8-inch Dynamic AMOLED display, 256GB storage.',
                        price=179999.00,
                        category_id=2,
                        stock=12,
                        features='Snapdragon 8 Gen 3, 6.8" Dynamic AMOLED, 256GB, Android 14'
                    ),
                    
                    # Accessories
                    Product(
                        name='AirPods Pro 2nd Gen',
                        description='Apple AirPods Pro 2nd generation with Active Noise Cancellation, Spatial Audio, and MagSafe charging case.',
                        price=29999.00,
                        category_id=3,
                        stock=25,
                        features='Active Noise Cancellation, Spatial Audio, MagSafe Case'
                    ),
                    Product(
                        name='Samsung Galaxy Watch 6',
                        description='Samsung Galaxy Watch 6 with 44mm display, health monitoring, GPS, and 2-day battery life.',
                        price=39999.00,
                        category_id=3,
                        stock=15,
                        features='44mm Display, Health Monitoring, GPS, 2-day Battery'
                    ),
                    
                    # Cyber Services
                    Product(
                        name='Website Security Audit',
                        description='Comprehensive security audit for your website including vulnerability assessment, penetration testing, and security recommendations.',
                        price=49999.00,
                        category_id=4,
                        stock=999,
                        features='Vulnerability Assessment, Penetration Testing, Security Report, Recommendations'
                    ),
                    Product(
                        name='Network Security Setup',
                        description='Complete network security setup including firewall configuration, VPN setup, and network monitoring tools.',
                        price=79999.00,
                        category_id=4,
                        stock=999,
                        features='Firewall Configuration, VPN Setup, Network Monitoring, Security Policies'
                    ),
                    Product(
                        name='Data Recovery Service',
                        description='Professional data recovery service for hard drives, SSDs, and other storage devices. High success rate recovery.',
                        price=29999.00,
                        category_id=4,
                        stock=999,
                        features='Hard Drive Recovery, SSD Recovery, High Success Rate, Secure Process'
                    )
                ]
                
                for product in products:
                    db.session.add(product)
                
                db.session.commit()
                print("✅ Products created")
                
                # Create admin user
                admin = User(
                    email='admin@kibtech.co.ke',
                    username='admin',
                    password='admin123',
                    is_admin=True,
                    referral_code='ADMIN001'
                )
                db.session.add(admin)
                
                # Create default commission rates
                commission_rate = CommissionRate(
                    rate=20.0,  # 20% commission
                    description='Default referral commission rate'
                )
                db.session.add(commission_rate)
                
                # Create default settings
                settings = Settings(
                    site_name='KibTech Store',
                    site_description='Premium Tech E-commerce Platform',
                    commission_rate=20.0,
                    min_withdrawal=100.0
                )
                db.session.add(settings)
                
                db.session.commit()
                print("✅ Admin user and settings created")
                
                print(f"✅ Database seeded successfully!")
                print(f"📊 Summary:")
                print(f"- Categories: {Category.query.count()}")
                print(f"- Products: {Product.query.count()}")
                print(f"- Admin Users: {User.query.filter_by(is_admin=True).count()}")
            else:
                print("✅ Database already has data")
            
            return True
            
    except Exception as e:
        print(f"❌ Error setting up Heroku database: {e}")
        return False

def setup_local_database():
    """Setup database for local development"""
    try:
        from app import create_app, db
        from app.models import User, Product, Category, CommissionRate, Settings
        
        app = create_app('local')
        
        with app.app_context():
            print("🚀 Setting up local database...")
            
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Check if we need to seed data
            product_count = Product.query.count()
            category_count = Category.query.count()
            
            if product_count == 0 or category_count == 0:
                print("🌱 Database is empty, seeding with default data...")
                
                # Create default categories
                categories = [
                    Category(name='Laptops', description='High-performance laptops for work and gaming'),
                    Category(name='Smartphones', description='Latest smartphones with advanced features'),
                    Category(name='Accessories', description='Essential tech accessories and peripherals'),
                    Category(name='Cyber Services', description='Professional cybersecurity and IT services')
                ]
                
                for category in categories:
                    db.session.add(category)
                
                db.session.commit()
                print("✅ Categories created")
                
                # Create default products (same as Heroku)
                products = [
                    # Laptops
                    Product(
                        name='MacBook Pro 14" M2',
                        description='Apple MacBook Pro with M2 chip, 14-inch Retina display, 16GB RAM, 512GB SSD.',
                        price=249999.00,
                        category_id=1,
                        stock=10,
                        features='M2 Chip, 14" Retina Display, 16GB RAM, 512GB SSD, macOS'
                    ),
                    Product(
                        name='Dell XPS 13 Plus',
                        description='Dell XPS 13 Plus with Intel i7, 13.4-inch OLED display, 16GB RAM, 512GB SSD.',
                        price=189999.00,
                        category_id=1,
                        stock=8,
                        features='Intel i7, 13.4" OLED, 16GB RAM, 512GB SSD, Windows 11'
                    ),
                    
                    # Smartphones
                    Product(
                        name='iPhone 15 Pro',
                        description='Apple iPhone 15 Pro with A17 Pro chip, 6.1-inch Super Retina XDR display, 256GB storage.',
                        price=189999.00,
                        category_id=2,
                        stock=20,
                        features='A17 Pro Chip, 6.1" Super Retina XDR, 256GB, iOS 17'
                    ),
                    Product(
                        name='Samsung Galaxy S24 Ultra',
                        description='Samsung Galaxy S24 Ultra with Snapdragon 8 Gen 3, 6.8-inch Dynamic AMOLED display, 256GB storage.',
                        price=179999.00,
                        category_id=2,
                        stock=12,
                        features='Snapdragon 8 Gen 3, 6.8" Dynamic AMOLED, 256GB, Android 14'
                    ),
                    
                    # Accessories
                    Product(
                        name='AirPods Pro 2nd Gen',
                        description='Apple AirPods Pro 2nd generation with Active Noise Cancellation, Spatial Audio, and MagSafe charging case.',
                        price=29999.00,
                        category_id=3,
                        stock=25,
                        features='Active Noise Cancellation, Spatial Audio, MagSafe Case'
                    ),
                    Product(
                        name='Samsung Galaxy Watch 6',
                        description='Samsung Galaxy Watch 6 with 44mm display, health monitoring, GPS, and 2-day battery life.',
                        price=39999.00,
                        category_id=3,
                        stock=15,
                        features='44mm Display, Health Monitoring, GPS, 2-day Battery'
                    ),
                    
                    # Cyber Services
                    Product(
                        name='Website Security Audit',
                        description='Comprehensive security audit for your website including vulnerability assessment, penetration testing, and security recommendations.',
                        price=49999.00,
                        category_id=4,
                        stock=999,
                        features='Vulnerability Assessment, Penetration Testing, Security Report, Recommendations'
                    ),
                    Product(
                        name='Network Security Setup',
                        description='Complete network security setup including firewall configuration, VPN setup, and network monitoring tools.',
                        price=79999.00,
                        category_id=4,
                        stock=999,
                        features='Firewall Configuration, VPN Setup, Network Monitoring, Security Policies'
                    ),
                    Product(
                        name='Data Recovery Service',
                        description='Professional data recovery service for hard drives, SSDs, and other storage devices. High success rate recovery.',
                        price=29999.00,
                        category_id=4,
                        stock=999,
                        features='Hard Drive Recovery, SSD Recovery, High Success Rate, Secure Process'
                    )
                ]
                
                for product in products:
                    db.session.add(product)
                
                db.session.commit()
                print("✅ Products created")
                
                # Create admin user
                admin = User(
                    email='admin@kibtech.co.ke',
                    username='admin',
                    password='admin123',
                    is_admin=True,
                    referral_code='ADMIN001'
                )
                db.session.add(admin)
                
                # Create default commission rates
                commission_rate = CommissionRate(
                    rate=20.0,  # 20% commission
                    description='Default referral commission rate'
                )
                db.session.add(commission_rate)
                
                # Create default settings
                settings = Settings(
                    site_name='KibTech Store',
                    site_description='Premium Tech E-commerce Platform',
                    commission_rate=20.0,
                    min_withdrawal=100.0
                )
                db.session.add(settings)
                
                db.session.commit()
                print("✅ Admin user and settings created")
                
                print(f"✅ Database seeded successfully!")
                print(f"📊 Summary:")
                print(f"- Categories: {Category.query.count()}")
                print(f"- Products: {Product.query.count()}")
                print(f"- Admin Users: {User.query.filter_by(is_admin=True).count()}")
            else:
                print("✅ Database already has data")
            
            return True
            
    except Exception as e:
        print(f"❌ Error setting up local database: {e}")
        return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database setup utility')
    parser.add_argument('--heroku', action='store_true', 
                       help='Setup for Heroku deployment')
    parser.add_argument('--local', action='store_true', 
                       help='Setup for local development')
    
    args = parser.parse_args()
    
    if args.heroku:
        print("🌐 Setting up database for Heroku deployment...")
        success = setup_heroku_database()
    elif args.local:
        print("💻 Setting up database for local development...")
        success = setup_local_database()
    else:
        # Default to local setup
        print("💻 Setting up database for local development...")
        success = setup_local_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("\n🌐 Access your store:")
        if args.heroku:
            print("- Production: https://kibtech.co.ke")
        else:
            print("- Local: http://localhost:5000")
            print("- Production: https://kibtech.co.ke")
        print("\n🔑 Admin Login:")
        print("- Email: admin@kibtech.co.ke")
        print("- Password: admin123 (change in production)")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 