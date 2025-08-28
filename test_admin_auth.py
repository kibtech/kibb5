#!/usr/bin/env python3
"""
Test admin authentication
"""
from app import create_app, db
from app.models import AdminUser, AdminRole
from app.admin.decorators import admin_required
from flask_jwt_extended import create_access_token
import bcrypt

def test_admin_auth():
    """Test admin authentication setup"""
    
    print("🔐 Testing Admin Authentication")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Check if admin users exist
            admin_users = AdminUser.query.all()
            print(f"📊 Found {len(admin_users)} admin users")
            
            for i, admin in enumerate(admin_users):
                print(f"  {i+1}. {admin.username} ({admin.email}) - Active: {admin.is_active}")
            
            # Check if admin roles exist
            admin_roles = AdminRole.query.all()
            print(f"📊 Found {len(admin_roles)} admin roles")
            
            for i, role in enumerate(admin_roles):
                print(f"  {i+1}. {role.name} - Active: {role.is_active}")
            
            # Test with first admin user
            if admin_users:
                admin = admin_users[0]
                print(f"\n🧪 Testing with admin: {admin.username}")
                
                # Create JWT token
                token = create_access_token(identity=admin.id)
                print(f"✅ JWT token created: {token[:20]}...")
                
                # Test admin_required decorator
                print("\n🔍 Testing admin_required decorator...")
                
                # Simulate request context
                with app.test_request_context():
                    # Set JWT identity
                    from flask_jwt_extended import get_jwt_identity
                    import flask_jwt_extended
                    
                    # Mock the JWT identity
                    flask_jwt_extended._get_jwt_identity = lambda: admin.id
                    
                    # Test the decorator
                    @admin_required
                    def test_function():
                        return "Success"
                    
                    try:
                        result = test_function()
                        print(f"✅ Decorator test passed: {result}")
                    except Exception as e:
                        print(f"❌ Decorator test failed: {str(e)}")
                
            else:
                print("❌ No admin users found!")
                print("💡 You may need to run fix_admin_setup.py")
            
            print("\n🎉 Admin authentication test completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_admin_auth()
    
    print("\n📝 Summary:")
    print("- Check if admin users exist")
    print("- Check if admin roles exist")
    print("- Verify JWT token creation")
    print("- Test admin_required decorator") 