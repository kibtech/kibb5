#!/usr/bin/env python3
"""
Test Cyber Services API and Database
"""

import os
import sys
import requests
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService, AdminUser

def test_database():
    """Test cyber services in database"""
    app = create_app()
    
    with app.app_context():
        print("🗄️  Testing Cyber Services Database...")
        
        # Check if cyber services exist
        services = CyberService.query.all()
        print(f"📊 Total cyber services in database: {len(services)}")
        
        if services:
            print("📋 Cyber Services found:")
            for service in services:
                print(f"   - {service.name} (ID: {service.id}, Active: {service.is_active})")
        else:
            print("❌ No cyber services found in database")
            
            # Create sample cyber services
            print("🔧 Creating sample cyber services...")
            sample_services = [
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
            
            for service_data in sample_services:
                service = CyberService(**service_data)
                db.session.add(service)
            
            db.session.commit()
            print("✅ Sample cyber services created!")
        
        # Check admin users
        admin_users = AdminUser.query.all()
        print(f"👥 Admin users: {len(admin_users)}")
        for admin in admin_users:
            print(f"   - {admin.email} (Active: {admin.is_active})")

def test_api_endpoint():
    """Test the API endpoint directly"""
    print("\n🌐 Testing API Endpoint...")
    
    # Test without authentication
    try:
        response = requests.get('http://localhost:5000/api/admin/cyber-services')
        print(f"📡 Response without auth: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly requires authentication")
        else:
            print(f"❌ Unexpected response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")

def main():
    """Main test function"""
    print("🧪 Cyber Services Test")
    print("=" * 50)
    
    # Test database
    test_database()
    
    # Test API endpoint
    test_api_endpoint()
    
    print("\n📋 Next Steps:")
    print("1. Start your Flask application: python app.py")
    print("2. Login to admin panel: http://localhost:5000/admin")
    print("3. Check cyber services page")
    print("4. If still getting 401, check browser network tab for JWT token")

if __name__ == "__main__":
    main() 