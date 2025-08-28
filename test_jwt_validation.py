#!/usr/bin/env python3
"""
Test JWT token validation
"""
import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import User, db
from flask_jwt_extended import create_access_token, decode_token

def test_jwt_validation():
    """Test JWT token creation and validation"""
    
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing JWT Token Validation...")
        print("=" * 50)
        
        # Find user JOY
        user = db.session.query(User).filter_by(name='JOY').first()
        if not user:
            print("❌ User 'JOY' not found!")
            return False
        
        print(f"✅ Found user: {user.name}")
        print(f"   User ID: {user.id}")
        print(f"   User ID type: {type(user.id)}")
        
        # Test token creation
        print(f"\n🔑 Testing JWT Token Creation...")
        try:
            token = create_access_token(identity=str(user.id))
            print(f"   ✅ Token created successfully")
            print(f"   Token length: {len(token)}")
            print(f"   Token preview: {token[:50]}...")
            
            # Test token decoding
            print(f"\n🔍 Testing Token Decoding...")
            decoded = decode_token(token)
            print(f"   ✅ Token decoded successfully")
            print(f"   Decoded identity: {decoded['sub']}")
            print(f"   Decoded identity type: {type(decoded['sub'])}")
            print(f"   Token type: {decoded['type']}")
            
            # Test with the actual token from the browser
            browser_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1NTE2OTUxNywianRpIjoiYTNlZGZiMjgtYmNkNC00OGVhLThiZGQtMDBkYmY3ZGNkMWQyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjI3IiwibmJmIjoxNzU1MTY5NTE3fQ.Kc1WgAYGZGMYl26VJJkucuHXw3GuIdcXsQLTJBlWEQk"
            
            print(f"\n🌐 Testing Browser Token...")
            try:
                browser_decoded = decode_token(browser_token)
                print(f"   ✅ Browser token decoded successfully")
                print(f"   Browser identity: {browser_decoded['sub']}")
                print(f"   Browser identity type: {type(browser_decoded['sub'])}")
                
                # Check if the identity matches
                if browser_decoded['sub'] == str(user.id):
                    print(f"   ✅ Token identity matches user ID")
                else:
                    print(f"   ❌ Token identity mismatch!")
                    print(f"      Token has: {browser_decoded['sub']}")
                    print(f"      User has: {user.id}")
                
            except Exception as e:
                print(f"   ❌ Browser token decode failed: {str(e)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating/decoding token: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("🚀 JWT Validation Tester")
    print("=" * 50)
    
    try:
        success = test_jwt_validation()
        if success:
            print("\n✅ JWT test completed successfully!")
        else:
            print("\n❌ JWT test failed!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc() 