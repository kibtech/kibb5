#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_flask_app():
    """Test the Flask app and its registered routes"""
    print("🔧 Testing Flask App Routes...")
    
    app = create_app()
    
    with app.app_context():
        try:
            print("📝 Registered blueprints:")
            for blueprint_name, blueprint in app.blueprints.items():
                print(f"  - {blueprint_name}: {blueprint.url_prefix}")
            
            print("\n📝 All registered routes:")
            for rule in app.url_map.iter_rules():
                print(f"  - {rule.rule} [{', '.join(rule.methods)}]")
            
            # Check specifically for wallet routes
            print("\n📝 Wallet routes:")
            wallet_routes = [rule for rule in app.url_map.iter_rules() if rule.rule.startswith('/api/wallet')]
            for route in wallet_routes:
                print(f"  - {route.rule} [{', '.join(route.methods)}]")
            
            if not wallet_routes:
                print("  ❌ No wallet routes found!")
            else:
                print(f"  ✅ Found {len(wallet_routes)} wallet routes")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing Flask app: {str(e)}")
            return False

if __name__ == "__main__":
    print("🚀 Flask App Routes Test Tool")
    print("=" * 50)
    
    success = test_flask_app()
    
    if success:
        print("\n✅ Flask app test completed!")
        print("💡 Check the output above to see all registered routes.")
    else:
        print("\n❌ Flask app test failed. Please check the error above.") 