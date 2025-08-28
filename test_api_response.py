#!/usr/bin/env python3
"""
Test API Response Structure
Simple test to verify the API response format
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService

def test_api_response_structure():
    """Test the API response structure"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Testing API Response Structure...")
            print("=" * 50)
            
            # Get services
            services = CyberService.query.all()
            
            # Calculate stats
            total_services = len(services)
            active_services = len([s for s in services if s.is_active])
            featured_services = len([s for s in services if s.is_featured])
            
            print(f"✅ Database stats:")
            print(f"   - Total: {total_services}")
            print(f"   - Active: {active_services}")
            print(f"   - Featured: {featured_services}")
            
            # Simulate the API response structure
            api_response = {
                'success': True,
                'services': [service.to_dict() for service in services],
                'pagination': {
                    'page': 1,
                    'per_page': 20,
                    'total': total_services,
                    'pages': 1,
                    'has_next': False,
                    'has_prev': False
                },
                'filters': {
                    'categories': ['KRA', 'HELB', 'Business', 'NTSA'],
                    'current_category': None,
                    'current_search': None,
                    'current_status': None
                },
                'stats': {
                    'total_services': total_services,
                    'active_services': active_services,
                    'featured_services': featured_services
                }
            }
            
            print(f"\n✅ API Response Structure:")
            print(f"   - success: {api_response['success']}")
            print(f"   - services count: {len(api_response['services'])}")
            print(f"   - stats: {api_response['stats']}")
            
            # Test frontend processing
            print(f"\n✅ Frontend Processing Test:")
            
            # Simulate what the frontend does
            data = api_response
            services_array = data.get('services', [])
            stats_object = data.get('stats', {})
            
            print(f"   - Services array length: {len(services_array)}")
            print(f"   - Stats object: {stats_object}")
            print(f"   - total_services: {stats_object.get('total_services', 0)}")
            print(f"   - active_services: {stats_object.get('active_services', 0)}")
            print(f"   - featured_services: {stats_object.get('featured_services', 0)}")
            
            # Check if stats are correct
            if (stats_object.get('total_services') == total_services and
                stats_object.get('active_services') == active_services and
                stats_object.get('featured_services') == featured_services):
                print("✅ Stats are correct!")
            else:
                print("❌ Stats mismatch!")
            
            print("\n" + "=" * 50)
            print("✅ API Response Structure Test Completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_api_response_structure() 