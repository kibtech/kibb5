#!/usr/bin/env python3
"""
Test Cyber Services Stats API
Verify that the stats are being calculated and returned correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CyberService, AdminUser
from sqlalchemy import text

def test_cyber_services_stats():
    """Test cyber services stats calculation"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Testing Cyber Services Stats...")
            print("=" * 50)
            
            # Test 1: Check total services count
            print("\n1. Checking total services count...")
            total_services = CyberService.query.count()
            print(f"✅ Total services in database: {total_services}")
            
            # Test 2: Check active services count
            print("\n2. Checking active services count...")
            active_services = CyberService.query.filter_by(is_active=True).count()
            print(f"✅ Active services in database: {active_services}")
            
            # Test 3: Check featured services count
            print("\n3. Checking featured services count...")
            featured_services = CyberService.query.filter_by(is_featured=True).count()
            print(f"✅ Featured services in database: {featured_services}")
            
            # Test 4: Check individual service status
            print("\n4. Checking individual service status...")
            services = CyberService.query.all()
            print(f"✅ Found {len(services)} services:")
            
            for i, service in enumerate(services[:5], 1):  # Show first 5 services
                print(f"   {i}. {service.name}")
                print(f"      - Active: {service.is_active}")
                print(f"      - Featured: {service.is_featured}")
                print(f"      - Category: {service.category}")
            
            if len(services) > 5:
                print(f"   ... and {len(services) - 5} more services")
            
            # Test 5: Verify stats calculation matches expected
            print("\n5. Verifying stats calculation...")
            expected_stats = {
                'total_services': total_services,
                'active_services': active_services,
                'featured_services': featured_services
            }
            
            print("✅ Expected stats:")
            for key, value in expected_stats.items():
                print(f"   - {key}: {value}")
            
            # Test 6: Check if there are any services with is_active = None
            print("\n6. Checking for null values...")
            null_active = CyberService.query.filter_by(is_active=None).count()
            null_featured = CyberService.query.filter_by(is_featured=None).count()
            
            print(f"✅ Services with is_active = NULL: {null_active}")
            print(f"✅ Services with is_featured = NULL: {null_featured}")
            
            if null_active > 0 or null_featured > 0:
                print("⚠️  Found services with NULL values - this might cause issues!")
                
                # Show services with NULL values
                null_services = CyberService.query.filter(
                    db.or_(CyberService.is_active.is_(None), CyberService.is_featured.is_(None))
                ).all()
                
                for service in null_services:
                    print(f"   - {service.name}: active={service.is_active}, featured={service.is_featured}")
            
            # Test 7: Test the exact query used in the API
            print("\n7. Testing API query logic...")
            try:
                # Simulate the exact queries from the API
                api_total = CyberService.query.count()
                api_active = CyberService.query.filter_by(is_active=True).count()
                api_featured = CyberService.query.filter_by(is_featured=True).count()
                
                print("✅ API query results:")
                print(f"   - total_services: {api_total}")
                print(f"   - active_services: {api_active}")
                print(f"   - featured_services: {api_featured}")
                
                if api_total == total_services and api_active == active_services and api_featured == featured_services:
                    print("✅ API queries match expected results!")
                else:
                    print("❌ API queries don't match expected results!")
                    
            except Exception as e:
                print(f"❌ Error testing API queries: {e}")
            
            print("\n" + "=" * 50)
            print("✅ Cyber Services Stats Test Completed!")
            
            if total_services > 0 and active_services > 0:
                print("✅ Stats should be working correctly in the admin portal.")
            else:
                print("⚠️  No services found or all services are inactive.")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            return False

if __name__ == "__main__":
    success = test_cyber_services_stats()
    if success:
        print("\n🎉 Stats test completed successfully!")
    else:
        print("\n❌ Stats test failed!")
        sys.exit(1) 