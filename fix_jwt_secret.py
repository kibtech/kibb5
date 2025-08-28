#!/usr/bin/env python3
"""
Fix JWT secret key issue
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, db
from flask_jwt_extended import create_access_token, decode_token

def fix_jwt_secret():
    """Fix JWT secret key issue"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Fixing JWT Secret Key Issue...")
        print("=" * 50)
        
        # Check current JWT configuration
        print(f"🔍 Current JWT Configuration:")
        print(f"   JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')}")
        print(f"   SECRET_KEY: {app.config.get('SECRET_KEY')}")
        
        # Find user JOY
        user = db.session.query(User).filter_by(name='JOY').first()
        if not user:
            print("❌ User 'JOY' not found!")
            return False
        
        print(f"\n✅ Found user: {user.name}")
        print(f"   User ID: {user.id}")
        
        # Test with current configuration
        print(f"\n🧪 Testing Current JWT Configuration...")
        try:
            token = create_access_token(identity=str(user.id))
            print(f"   ✅ Token created with current config")
            
            # Try to decode it
            decoded = decode_token(token)
            print(f"   ✅ Token decoded successfully")
            print(f"   Identity: {decoded['sub']}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return False
        
        # Check if we need to set a consistent JWT secret
        current_jwt_secret = app.config.get('JWT_SECRET_KEY')
        if current_jwt_secret == 'your-super-secret-jwt-key-here':
            print(f"\n⚠️  JWT_SECRET_KEY is using default value!")
            print(f"   This will cause authentication issues.")
            
            # Set a consistent JWT secret
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
                
            except Exception as e:
                print(f"   ❌ Error with new config: {str(e)}")
                return False
        
        return True

if __name__ == "__main__":
    print("🚀 JWT Secret Key Fixer")
    print("=" * 50)
    
    try:
        success = fix_jwt_secret()
        if success:
            print("\n✅ JWT fix completed!")
        else:
            print("\n❌ JWT fix failed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 