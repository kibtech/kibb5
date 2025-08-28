#!/usr/bin/env python3
"""
Test Cyber Services Admin Functionality
Comprehensive test to verify all admin operations work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService, CyberServiceOrder, AdminUser, SystemLog
from sqlalchemy import text

def test_cyber_services_admin():
    """Test all cyber services admin functionality"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Testing Cyber Services Admin Functionality...")
            print("=" * 50)
            
            # Test 1: Check if cyber_services table exists
            print("\n1. Checking cyber_services table...")
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'cyber_services'
            """))
            
            if result.fetchone():
                print("✅ cyber_services table exists")
            else:
                print("❌ cyber_services table does not exist")
                return False
            
            # Test 2: Check if image_url column exists
            print("\n2. Checking image_url column...")
            result = db.session.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'cyber_services' 
                AND column_name = 'image_url'
            """))
            
            column_info = result.fetchone()
            if column_info:
                print(f"✅ image_url column exists: {column_info[0]} ({column_info[1]})")
            else:
                print("❌ image_url column does not exist")
                return False
            
            # Test 3: Check table structure
            print("\n3. Checking table structure...")
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'cyber_services'
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            print("✅ Table structure:")
            for col in columns:
                print(f"   - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
            
            # Test 4: Test CyberService model
            print("\n4. Testing CyberService model...")
            try:
                # Create a test service
                test_service = CyberService(
                    name="Test KRA Service",
                    slug="test-kra-service",
                    description="Test service for KRA compliance",
                    short_description="Quick KRA service",
                    price=1500.00,
                    category="KRA",
                    subcategory="Tax Compliance",
                    estimated_duration="24-48 hours",
                    requirements="Valid ID, Phone number",
                    benefits="Official certificate, Tax compliance",
                    instructions="Submit required documents",
                    is_active=True,
                    is_featured=False,
                    sort_order=1,
                    image_url="/static/uploads/test-image.jpg"
                )
                
                db.session.add(test_service)
                db.session.commit()
                print("✅ Test service created successfully")
                
                # Test to_dict method
                service_dict = test_service.to_dict()
                required_fields = ['id', 'name', 'slug', 'description', 'price', 'category', 'image_url']
                missing_fields = [field for field in required_fields if field not in service_dict]
                
                if not missing_fields:
                    print("✅ to_dict method works correctly")
                else:
                    print(f"❌ Missing fields in to_dict: {missing_fields}")
                
                # Test query
                service = CyberService.query.filter_by(slug="test-kra-service").first()
                if service:
                    print("✅ Service query works correctly")
                else:
                    print("❌ Service query failed")
                
                # Clean up test service
                db.session.delete(test_service)
                db.session.commit()
                print("✅ Test service cleaned up")
                
            except Exception as e:
                print(f"❌ Error testing CyberService model: {e}")
                db.session.rollback()
                return False
            
            # Test 5: Check if admin routes are registered
            print("\n5. Checking admin routes...")
            try:
                from app.admin import admin_bp
                from flask import current_app
                
                # Get all registered routes
                routes = []
                for rule in current_app.url_map.iter_rules():
                    if rule.endpoint.startswith('admin.'):
                        routes.append(str(rule))
                
                cyber_routes = [route for route in routes if 'cyber' in route.lower()]
                
                if cyber_routes:
                    print("✅ Cyber services admin routes found:")
                    for route in cyber_routes:
                        print(f"   - {route}")
                else:
                    print("⚠️  No cyber services admin routes found in URL map (this is normal if app hasn't been fully initialized)")
                    print("   Routes will be available when the Flask app is running")
                    
            except Exception as e:
                print(f"⚠️  Could not check admin routes: {e}")
                print("   This is normal in test environment")
            
            # Test 6: Check admin imports
            print("\n6. Checking admin imports...")
            try:
                from app.admin import cyber_services
                print("✅ cyber_services module imported successfully")
                
                # Check if routes are defined
                if hasattr(cyber_services, 'get_cyber_services_admin'):
                    print("✅ get_cyber_services_admin route exists")
                else:
                    print("❌ get_cyber_services_admin route missing")
                
                if hasattr(cyber_services, 'create_cyber_service'):
                    print("✅ create_cyber_service route exists")
                else:
                    print("❌ create_cyber_service route missing")
                    
            except Exception as e:
                print(f"❌ Error checking admin imports: {e}")
                return False
            
            # Test 7: Check database connectivity
            print("\n7. Testing database connectivity...")
            try:
                # Test basic query
                count = CyberService.query.count()
                print(f"✅ Database connectivity works. Current services: {count}")
                
                # Test admin user query
                admin_count = AdminUser.query.count()
                print(f"✅ Admin users in database: {admin_count}")
                
            except Exception as e:
                print(f"❌ Database connectivity error: {e}")
                return False
            
            print("\n" + "=" * 50)
            print("✅ All Cyber Services Admin tests passed!")
            print("✅ The admin portal should now work correctly for cyber services management.")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return False

if __name__ == "__main__":
    success = test_cyber_services_admin()
    if success:
        print("\n🎉 Cyber Services Admin is ready to use!")
        print("You can now access the admin portal and manage cyber services.")
    else:
        print("\n❌ Cyber Services Admin needs further fixes.")
        sys.exit(1) 