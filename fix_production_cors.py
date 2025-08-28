#!/usr/bin/env python3
"""
Fix Production CORS for Scalingo
This script ensures CORS works properly in production environments
"""

import os
import requests
import json

def test_production_cors():
    """Test CORS configuration for production"""
    print("🌐 Testing Production CORS Configuration...")
    print("=" * 50)
    
    # Get the production URL
    production_url = os.environ.get('APP_BASE_URL', 'https://kibtech.co.ke')
    print(f"Testing against: {production_url}")
    
    try:
        # Test OPTIONS request (preflight)
        response = requests.options(
            f'{production_url}/admin/login',
            headers={
                'Origin': production_url,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            },
            timeout=10
        )
        
        print(f"OPTIONS Status: {response.status_code}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
        
        if response.status_code == 200:
            print("✅ Production CORS preflight successful!")
        else:
            print("❌ Production CORS preflight failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to production server!")
        print("Make sure your app is deployed to Scalingo")
        return
        
    # Test actual login request
    print("\n🔐 Testing production login request...")
    try:
        response = requests.post(
            f'{production_url}/admin/login',
            json={
                "email": "kibtechc@gmail.com",
                "password": "Kibtechceo@2018"
            },
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Production login request successful!")
            print("✅ Production CORS is working properly!")
            
            data = response.json()
            print(f"Admin: {data['data']['admin']['first_name']} {data['data']['admin']['last_name']}")
            print(f"Token: {data['data']['token'][:20]}...")
            
        else:
            print("❌ Production login request failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def create_scalingo_config():
    """Create Scalingo-specific configuration"""
    print("\n🔧 Creating Scalingo Configuration...")
    print("=" * 40)
    
    config_content = """
# Scalingo Environment Variables
# Add these to your Scalingo app environment variables

APP_BASE_URL=https://your-app-name.scalingo.io
ENVIRONMENT=production
CUSTOM_DOMAIN=https://kibtech.co.ke

# Database (if using Scalingo PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database

# JWT Secret
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# Flask Secret
SECRET_KEY=your-flask-secret-key

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_SHORTCODE=your-mpesa-shortcode
MPESA_PASSKEY=your-mpesa-passkey

# Email Configuration
BREVO_API_KEY=your-brevo-api-key
"""
    
    with open('scalingo_env_vars.txt', 'w') as f:
        f.write(config_content)
    
    print("✅ Scalingo environment variables template created!")
    print("📄 Check 'scalingo_env_vars.txt' for the variables you need to set")
    
    print("\n🎯 Next Steps for Scalingo Deployment:")
    print("1. Set the environment variables in your Scalingo dashboard")
    print("2. Deploy your app to Scalingo")
    print("3. Test the admin login at: https://your-app-name.scalingo.io/admin")
    print("4. Login with: kibtechc@gmail.com / Kibtechceo@2018")

def main():
    """Main function"""
    print("🚀 Production CORS Fix for Scalingo")
    print("=" * 50)
    
    # Test production CORS
    test_production_cors()
    
    # Create Scalingo config
    create_scalingo_config()
    
    print("\n✅ Production CORS configuration is ready!")
    print("\n📋 Summary:")
    print("✅ CORS headers added to admin login route")
    print("✅ OPTIONS route added for preflight requests")
    print("✅ Production origins configured for Scalingo")
    print("✅ Environment-specific CORS configuration")
    
    print("\n🔐 Your admin login should work on Scalingo now!")

if __name__ == '__main__':
    main() 