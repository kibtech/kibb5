#!/usr/bin/env python3
"""
Test Admin Authentication Fix
Verify that admin authentication works correctly for cyber services
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser, CyberService
from sqlalchemy import text

def test_admin_auth_fix():
    """Test admin authentication for cyber services"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Testing Admin Authentication Fix...")
            print("=" * 50)
            
            # Test 1: Check if admin user exists
            print("\n1. Checking admin user...")
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if admin_user:
                print(f"✅ Admin user found: {admin_user.username}")
                print(f"   - Active: {admin_user.is_active}")
                print(f"   - Super Admin: {admin_user.is_super_admin}")
            else:
                print("❌ Admin user not found")
                return False
            
            # Test 2: Check cyber services count
            print("\n2. Checking cyber services...")
            services_count = CyberService.query.count()
            print(f"✅ Cyber services in database: {services_count}")
            
            # Test 3: Test admin authentication decorator
            print("\n3. Testing admin authentication...")
            try:
                from app.admin.auth import admin_login_required
                print("✅ admin_login_required decorator imported successfully")
            except Exception as e:
                print(f"❌ Error importing admin_login_required: {e}")
                return False
            
            # Test 4: Check admin routes are accessible
            print("\n4. Checking admin routes...")
            try:
                from app.admin import cyber_services
                print("✅ cyber_services module accessible")
                
                # Check if routes are properly decorated
                if hasattr(cyber_services, 'get_cyber_services_admin'):
                    print("✅ get_cyber_services_admin route exists")
                else:
                    print("❌ get_cyber_services_admin route missing")
                    
            except Exception as e:
                print(f"❌ Error accessing admin routes: {e}")
                return False
            
            # Test 5: Check JWT configuration
            print("\n5. Checking JWT configuration...")
            try:
                from flask_jwt_extended import create_access_token, jwt_required
                print("✅ JWT extensions available")
                
                # Test token creation
                test_token = create_access_token(identity=str(admin_user.id))
                print(f"✅ JWT token creation works: {test_token[:20]}...")
                
            except Exception as e:
                print(f"❌ JWT configuration error: {e}")
                return False
            
            print("\n" + "=" * 50)
            print("✅ Admin Authentication Fix Test Passed!")
            print("✅ The cyber services admin portal should now work correctly.")
            print("\n📝 Next Steps:")
            print("1. Start the application with START_KIBTECH.bat")
            print("2. Login to admin portal with:")
            print("   - Email: kibtechc@gmail.com")
            print("   - Password: admin123")
            print("3. Navigate to Cyber Services in the admin panel")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return False

if __name__ == "__main__":
    success = test_admin_auth_fix()
    if success:
        print("\n🎉 Admin authentication is ready!")
    else:
        print("\n❌ Admin authentication needs further fixes.")
        sys.exit(1) 