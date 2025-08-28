#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask_jwt_extended import create_access_token, decode_token
import jwt

def test_jwt_secret():
    """Test JWT secret key configuration"""
    app = create_app()
    
    with app.app_context():
        print("Testing JWT configuration...")
        print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
        print(f"JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')}")
        
        # Test creating a token
        user_id = 6  # kashdyke@gmail.com user ID
        token = create_access_token(identity=user_id)
        print(f"Token created: {token[:50]}...")
        
        # Try to decode with JWT_SECRET_KEY
        try:
            decoded = jwt.decode(token, app.config.get('JWT_SECRET_KEY'), algorithms=['HS256'])
            print(f"✅ Token decoded with JWT_SECRET_KEY: {decoded}")
        except Exception as e:
            print(f"❌ Failed to decode with JWT_SECRET_KEY: {e}")
        
        # Try to decode with SECRET_KEY
        try:
            decoded = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
            print(f"✅ Token decoded with SECRET_KEY: {decoded}")
        except Exception as e:
            print(f"❌ Failed to decode with SECRET_KEY: {e}")
        
        # Test with flask-jwt-extended decode
        try:
            decoded = decode_token(token)
            print(f"✅ Token decoded with flask-jwt-extended: {decoded}")
        except Exception as e:
            print(f"❌ Failed to decode with flask-jwt-extended: {e}")

if __name__ == '__main__':
    test_jwt_secret() 