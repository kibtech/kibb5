#!/usr/bin/env python3
"""
Test script to check route registration
"""

from app import create_app

def test_route_registration():
    """Test if cyber services routes are properly registered"""
    app = create_app()
    
    print("🔍 Checking route registration...")
    print("=" * 50)
    
    # Check all routes
    cyber_routes = []
    for rule in app.url_map.iter_rules():
        if 'cyber' in rule.rule:
            cyber_routes.append(rule.rule)
    
    print(f"Found {len(cyber_routes)} cyber-related routes:")
    for route in cyber_routes:
        print(f"  {route}")
    
    # Check specific routes we expect
    expected_routes = [
        '/api/cyber-services/services',
        '/api/cyber-services/categories',
        '/api/cyber-services/services/<slug>'
    ]
    
    print("\nChecking expected routes:")
    for expected in expected_routes:
        if expected in cyber_routes:
            print(f"  ✅ {expected}")
        else:
            print(f"  ❌ {expected} - NOT FOUND")
    
    print("\n" + "=" * 50)

if __name__ == '__main__':
    test_route_registration() 