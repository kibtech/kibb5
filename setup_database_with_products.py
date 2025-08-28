#!/usr/bin/env python3
"""
Enhanced Database Setup Script for KIBTECH ONLINE SERVICES
This script sets up the database and automatically seeds all default products
Run with: python setup_database_with_products.py
"""

import os
import sys
import shutil
from flask import Flask

def setup_database_with_products():
    """Set up the database with all tables and automatically seed default products"""
    
    print("🚀 Setting up KIBTECH ONLINE SERVICES database with default products...")
    
    # Clean up old migration files and instance directory
    migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations')
    instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
    
    if os.path.exists(migrations_dir):
        print("🧹 Cleaning up old migration files...")
        try:
            shutil.rmtree(migrations_dir)
        except Exception as e:
            print(f"Warning: Could not remove migrations directory: {e}")
    
    if os.path.exists(instance_dir):
        print("🧹 Cleaning up instance directory...")
        try:
            shutil.rmtree(instance_dir)
        except Exception as e:
            print(f"Warning: Could not remove instance directory: {e}")
    
    # Import after cleaning up
    try:
        from app import create_app, db
        
        # Create Flask app
        app = create_app()
        
        with app.app_context():
            print("📋 Creating database tables...")
            
            # Create all tables
            db.create_all()
            
            print("✅ Database tables created successfully!")
            
            # Auto-seed with default products
            try:
                from auto_seed_products import auto_seed_database
                print("🌱 Auto-seeding database with default products...")
                auto_seed_database()
                print("✅ Default products added successfully!")
            except Exception as e:
                print(f"⚠️  Warning: Could not auto-seed products: {e}")
                print("You can run 'python auto_seed_products.py' manually later.")
            
            print("\n🎉 KIBTECH ONLINE SERVICES database setup completed!")
            print("🌐 Your platform is ready to use with all default products!")
            print("\n📦 Default products available:")
            print("- Smartphones (Samsung Galaxy A54 5G, iPhone 14 Pro)")
            print("- Laptops (Dell XPS 13, HP Spectre x360)")
            print("- Audio (Sony WH-1000XM4, Apple AirPods Pro)")
            print("- Cameras (Canon EOS R6 Mark II)")
            print("- Tablets (iPad Air)")
            print("- Accessories (Apple AirPods Pro)")
            
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n💡 Try running the following commands manually:")
        print("   1. python setup_database_with_products.py")
        print("   2. python auto_seed_products.py")
        sys.exit(1)

if __name__ == '__main__':
    setup_database_with_products() 