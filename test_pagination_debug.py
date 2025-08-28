#!/usr/bin/env python3
"""
Test Pagination Debug
=====================

This script tests the backend pagination to see if it's working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from sqlalchemy import func

def test_backend_pagination():
    """Test if backend pagination is working"""
    print("🧪 Testing Backend Pagination")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Test pagination logic
            print("\n1. 🔍 Testing pagination logic...")
            
            total_users = User.query.count()
            print(f"   Total users in database: {total_users}")
            
            # Test page 1
            page1_users = User.query.paginate(page=1, per_page=20, error_out=False)
            print(f"   Page 1: {len(page1_users.items)} users")
            print(f"   Page 1 pagination: {page1_users.page} of {page1_users.pages}")
            print(f"   Has next: {page1_users.has_next}")
            print(f"   Has prev: {page1_users.has_prev}")
            
            # Test page 2 if it exists
            if page1_users.has_next:
                page2_users = User.query.paginate(page=2, per_page=20, error_out=False)
                print(f"   Page 2: {len(page2_users.items)} users")
                print(f"   Page 2 pagination: {page2_users.page} of {page2_users.pages}")
                print(f"   Has next: {page2_users.has_next}")
                print(f"   Has prev: {page2_users.has_prev}")
            else:
                print(f"   ⚠️ No page 2 available")
            
            # Test the exact response format
            print(f"\n2. 🔍 Testing response format...")
            
            # Simulate the exact backend response
            pagination = page1_users
            response_data = {
                'users': [user.to_dict() for user in pagination.items],
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
            print(f"   Response structure:")
            print(f"      Users count: {len(response_data['users'])}")
            print(f"      Pagination object: {response_data['pagination']}")
            
            # Test if pagination object has all required fields
            required_fields = ['page', 'per_page', 'total', 'pages', 'has_next', 'has_prev']
            missing_fields = [field for field in required_fields if field not in response_data['pagination']]
            
            if missing_fields:
                print(f"   ❌ Missing pagination fields: {missing_fields}")
            else:
                print(f"   ✅ All required pagination fields present")
            
            # Test page calculation
            expected_pages = (total_users + 19) // 20  # Ceiling division
            actual_pages = response_data['pagination']['pages']
            
            print(f"\n3. 🔍 Testing page calculation...")
            print(f"   Expected pages: {expected_pages}")
            print(f"   Actual pages: {actual_pages}")
            print(f"   Match: {'✅' if expected_pages == actual_pages else '❌'}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error testing pagination: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Backend Pagination Test")
    print("=" * 50)
    
    success = test_backend_pagination()
    
    if success:
        print("\n🎉 Backend pagination test completed!")
        print("\n📋 If backend is working, the issue is in the frontend.")
        print("   Check browser console for JavaScript errors.")
    else:
        print("\n❌ Backend pagination test failed!") 