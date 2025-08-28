#!/usr/bin/env python3
"""
Test Cyber Services API Endpoint
Directly test the API endpoint to see what it returns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService, AdminUser
from app.admin.cyber_services import get_cyber_services_admin
from flask import json

def test_cyber_services_api():
    """Test the cyber services API endpoint directly"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Testing Cyber Services API Endpoint...")
            print("=" * 50)
            
            # Test 1: Check if admin user exists
            print("\n1. Checking admin user...")
            admin_user = AdminUser.query.filter_by(email='kibtechc@gmail.com').first()
            
            if not admin_user:
                print("❌ Admin user not found")
                return False
            
            print(f"✅ Admin user found: {admin_user.username}")
            
            # Test 2: Check services count
            print("\n2. Checking services count...")
            total_services = CyberService.query.count()
            active_services = CyberService.query.filter_by(is_active=True).count()
            featured_services = CyberService.query.filter_by(is_featured=True).count()
            
            print(f"✅ Total services: {total_services}")
            print(f"✅ Active services: {active_services}")
            print(f"✅ Featured services: {featured_services}")
            
            # Test 3: Test the API function directly
            print("\n3. Testing API function...")
            try:
                # Create a mock request context
                with app.test_request_context('/api/admin/cyber-services'):
                    # Mock the admin_required decorator by setting current_user
                    from flask_login import login_user
                    login_user(admin_user)
                    
                    # Call the function directly
                    response = get_cyber_services_admin()
                    
                    if response:
                        print("✅ API function executed successfully")
                        print(f"Response type: {type(response)}")
                        
                        # Try to get the response data
                        if hasattr(response, 'get_json'):
                            data = response.get_json()
                        elif hasattr(response, 'json'):
                            data = response.json
                        else:
                            data = response
                        
                        print(f"Response data: {data}")
                        
                        if isinstance(data, dict):
                            print(f"Services count: {len(data.get('services', []))}")
                            print(f"Stats: {data.get('stats', {})}")
                        else:
                            print(f"Unexpected response format: {data}")
                    else:
                        print("❌ API function returned None")
                        
            except Exception as e:
                print(f"❌ Error testing API function: {e}")
                import traceback
                traceback.print_exc()
            
            # Test 4: Check the actual database query
            print("\n4. Testing database query...")
            services = CyberService.query.all()
            print(f"✅ Retrieved {len(services)} services from database")
            
            # Calculate stats manually
            total = len(services)
            active = len([s for s in services if s.is_active])
            featured = len([s for s in services if s.is_featured])
            
            print(f"✅ Manual stats calculation:")
            print(f"   - Total: {total}")
            print(f"   - Active: {active}")
            print(f"   - Featured: {featured}")
            
            print("\n" + "=" * 50)
            print("✅ Cyber Services API Test Completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    test_cyber_services_api() 