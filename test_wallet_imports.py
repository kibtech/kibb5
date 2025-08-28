#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_wallet_imports():
    """Test wallet imports step by step"""
    print("🔧 Testing Wallet Imports...")
    
    try:
        # Test basic imports
        print("📝 Testing basic imports...")
        from flask import Blueprint, jsonify, request
        print("✅ Flask imports OK")
        
        from flask_jwt_extended import jwt_required, get_jwt_identity
        print("✅ JWT imports OK")
        
        from app.models import User, Wallet, Commission, Withdrawal, Deposit
        print("✅ Model imports OK")
        
        from app.auth.decorators import email_verification_required
        print("✅ Decorator import OK")
        
        from app import db
        print("✅ DB import OK")
        
        from decimal import Decimal
        print("✅ Decimal import OK")
        
        # Test creating blueprint
        print("\n📝 Testing blueprint creation...")
        bp = Blueprint('wallet', __name__)
        print("✅ Blueprint created")
        
        # Test importing routes
        print("\n📝 Testing routes import...")
        import app.wallet.routes
        print("✅ Routes imported")
        
        # Check if routes were registered
        print(f"📝 Number of routes: {len(bp.deferred_functions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during import test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Wallet Imports Test Tool")
    print("=" * 50)
    
    success = test_wallet_imports()
    
    if success:
        print("\n✅ Wallet imports test completed!")
    else:
        print("\n❌ Wallet imports test failed. Please check the error above.") 