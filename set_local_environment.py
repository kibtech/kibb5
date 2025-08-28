#!/usr/bin/env python3
"""
Set Local Environment
This script helps set the environment for local development
"""

import os

def set_local_environment():
    """Set environment for local development"""
    print("🏠 Setting Local Development Environment")
    print("=" * 40)
    
    # Set environment variables for local development
    os.environ['ENVIRONMENT'] = 'development'
    
    # Remove APP_BASE_URL if it exists (to avoid confusion)
    if 'APP_BASE_URL' in os.environ:
        del os.environ['APP_BASE_URL']
        print("✅ Removed APP_BASE_URL (not needed for local development)")
    
    print("✅ Environment set for local development")
    print("   ENVIRONMENT=development")
    print("   APP_BASE_URL=unset (will use localhost)")
    
    print("\n🎯 Next Steps:")
    print("1. Start your server: python run.py")
    print("2. Auto CORS test will detect local environment")
    print("3. Test localhost URLs: http://localhost:5000/admin")
    
    print("\n📋 Expected Auto CORS Test Output:")
    print("   🏠 Auto CORS Test: Local Development Environment")
    print("   ✅ Auto CORS Test: OPTIONS request successful")
    print("   ✅ Auto CORS Test: Login request successful")
    print("   🎯 Admin login ready at: http://localhost:5000/admin")

def set_production_environment():
    """Set environment for production"""
    print("🌐 Setting Production Environment")
    print("=" * 40)
    
    # Set environment variables for production
    os.environ['ENVIRONMENT'] = 'production'
    os.environ['APP_BASE_URL'] = 'https://kibtech.co.ke'
    
    print("✅ Environment set for production")
    print("   ENVIRONMENT=production")
    print("   APP_BASE_URL=https://kibtech.co.ke")
    
    print("\n🎯 Next Steps:")
    print("1. Deploy to Scalingo with these environment variables")
    print("2. Auto CORS test will detect production environment")
    print("3. Test production URL: https://kibtech.co.ke/admin")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'production':
        set_production_environment()
    else:
        set_local_environment() 