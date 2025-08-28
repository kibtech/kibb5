#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import jwt

def test_jwt_manual():
    """Manually test JWT token creation and validation"""
    app = create_app()
    
    with app.app_context():
        print("Testing JWT manually...")
        
        # Create a token
        user_id = 6
        token = create_access_token(identity=user_id)
        print(f"Token created: {token[:50]}...")
        
        # Try to decode manually
        try:
            decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            print(f"✅ Manual decode successful: {decoded}")
        except Exception as e:
            print(f"❌ Manual decode failed: {e}")
        
        # Test with flask-jwt-extended
        try:
            from flask_jwt_extended import decode_token
            decoded = decode_token(token)
            print(f"✅ Flask-JWT decode successful: {decoded}")
        except Exception as e:
            print(f"❌ Flask-JWT decode failed: {e}")
        
        # Test the @jwt_required decorator
        @jwt_required()
        def test_protected_route():
            current_user_id = get_jwt_identity()
            return f"User ID: {current_user_id}"
        
        # This should work in the app context
        try:
            result = test_protected_route()
            print(f"✅ Protected route test: {result}")
        except Exception as e:
            print(f"❌ Protected route test failed: {e}")

if __name__ == '__main__':
    test_jwt_manual() 