#!/usr/bin/env python3
"""
Fix JWT configuration across all blueprints
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db, jwt
from app.models import User
from flask_jwt_extended import create_access_token, decode_token

def fix_jwt_blueprint_issue():
    """Fix JWT configuration across all blueprints"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Fixing JWT Blueprint Configuration...")
        print("=" * 60)
        
        # Check current JWT configuration
        print(f"🔍 Current JWT Configuration:")
        print(f"   JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')}")
        print(f"   JWT_ALGORITHM: {app.config.get('JWT_ALGORITHM')}")
        print(f"   JWT_ACCESS_TOKEN_EXPIRES: {app.config.get('JWT_ACCESS_TOKEN_EXPIRES')}")
        
        # Check if JWT manager is properly initialized
        print(f"\n🔍 JWT Manager Status:")
        print(f"   JWT Manager initialized: {jwt is not None}")
        
        # Find user JOY
        user = db.session.query(User).filter_by(name='JOY').first()
        if not user:
            print("❌ User 'JOY' not found!")
            return False
        
        print(f"\n✅ Found user: {user.name}")
        print(f"   User ID: {user.id}")
        
        # Test JWT token creation and validation
        print(f"\n🧪 Testing JWT Token...")
        try:
            token = create_access_token(identity=str(user.id))
            print(f"   ✅ Token created successfully")
            
            # Decode the token
            decoded = decode_token(token)
            print(f"   ✅ Token decoded successfully")
            print(f"   Identity: {decoded['sub']}")
            print(f"   Token type: {decoded['type']}")
            
        except Exception as e:
            print(f"   ❌ JWT error: {str(e)}")
            return False
        
        # Check if the issue is with the JWT secret key
        current_jwt_secret = app.config.get('JWT_SECRET_KEY')
        if 'your-super-secret-jwt-key-here' in current_jwt_secret:
            print(f"\n⚠️  JWT_SECRET_KEY is using default value!")
            print(f"   This is causing the authentication issues.")
            
            # Generate a new secure JWT secret
            import secrets
            new_jwt_secret = secrets.token_hex(32)
            
            print(f"\n🔧 Setting new JWT_SECRET_KEY...")
            print(f"   New secret: {new_jwt_secret}")
            
            # Update the config
            app.config['JWT_SECRET_KEY'] = new_jwt_secret
            
            # Test with new secret
            print(f"\n🧪 Testing New JWT Configuration...")
            try:
                new_token = create_access_token(identity=str(user.id))
                print(f"   ✅ New token created")
                
                new_decoded = decode_token(new_token)
                print(f"   ✅ New token decoded successfully")
                print(f"   Identity: {new_decoded['sub']}")
                
                print(f"\n✅ JWT configuration fixed!")
                print(f"   Please set this environment variable:")
                print(f"   JWT_SECRET_KEY={new_jwt_secret}")
                
                print(f"\n🔥 IMPORTANT: Restart your Flask server after setting the environment variable!")
                
            except Exception as e:
                print(f"   ❌ Error with new config: {str(e)}")
                return False
        
        return True

if __name__ == "__main__":
    print("🚀 JWT Blueprint Fixer")
    print("=" * 60)
    
    try:
        success = fix_jwt_blueprint_issue()
        if success:
            print("\n✅ JWT blueprint fix completed!")
        else:
            print("\n❌ JWT blueprint fix failed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 