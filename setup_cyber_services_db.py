#!/usr/bin/env python3
"""
Setup script for Cyber Services database tables and seed data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService, CyberServiceOrder, CyberServiceForm

def setup_database():
    """Create database tables for cyber services"""
    print("🔧 Setting up database tables...")
    
    app = create_app()
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            return False

def verify_setup():
    """Verify that the setup was successful"""
    print("🔍 Verifying setup...")
    
    app = create_app()
    with app.app_context():
        try:
            # Check if tables exist
            cyber_services_count = CyberService.query.count()
            print(f"📊 Found {cyber_services_count} cyber services in database")
            
            if cyber_services_count > 0:
                print("✅ Cyber services setup completed successfully!")
                return True
            else:
                print("❌ No services found. Setup may have failed.")
                return False
        except Exception as e:
            print(f"❌ Error verifying setup: {e}")
            return False

def main():
    print("=" * 50)
    print("    KIBTECH CYBER SERVICES SETUP")
    print("=" * 50)
    print()
    
    # Step 1: Setup database tables
    if not setup_database():
        print("❌ Database setup failed!")
        return
    
    print()
    
    # Step 2: Seed cyber services
    print("🌱 Seeding cyber services...")
    try:
        from seed_cyber_services import seed_cyber_services
        seed_cyber_services()
    except Exception as e:
        print(f"❌ Error seeding services: {e}")
        return
    
    print()
    
    # Step 3: Verify setup
    if not verify_setup():
        print("❌ Setup verification failed!")
        return
    
    print()
    print("🎉 Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Start your backend server: python run.py")
    print("2. Start your frontend: cd frontend && npm start")
    print("3. Visit https://kibtech.coke/cyber-services")
    print()

if __name__ == '__main__':
    main() 