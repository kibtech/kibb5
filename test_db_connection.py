#!/usr/bin/env python3
"""
Test PostgreSQL database connection and provide alternatives
"""

import os
import sys
import psycopg2
from urllib.parse import urlparse

def test_railway_connection():
    """Test the Railway PostgreSQL connection"""
    print("🔍 Testing Railway PostgreSQL connection...")
    
    # Railway connection details
    railway_url = "postgresql://postgres:UyAUrqMDtsFssWrwYdYRaqNfNMFpNbqW@trolley.proxy.rlwy.net:20673/railway"
    
    try:
        # Parse the URL
        parsed = urlparse(railway_url)
        
        # Test connection
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password,
            connect_timeout=10
        )
        
        # Test a simple query
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        
        cur.close()
        conn.close()
        
        print("✅ Railway PostgreSQL connection successful!")
        print(f"📊 Database version: {version[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Railway connection failed: {str(e)}")
        return False

def test_local_postgres():
    """Test local PostgreSQL connection"""
    print("\n🔍 Testing local PostgreSQL connection...")
    
    try:
        # Try common local PostgreSQL configurations
        local_configs = [
            "postgresql://postgres:password@localhost:5432/kibtech",
            "postgresql://kibtech:password@localhost:5432/kibtech",
            "postgresql://postgres@localhost:5432/kibtech"
        ]
        
        for config in local_configs:
            try:
                parsed = urlparse(config)
                conn = psycopg2.connect(
                    host=parsed.hostname,
                    port=parsed.port,
                    database=parsed.path[1:],
                    user=parsed.username,
                    password=parsed.password,
                    connect_timeout=5
                )
                conn.close()
                print(f"✅ Local PostgreSQL connection successful with: {config}")
                return config
            except:
                continue
                
        print("❌ No local PostgreSQL connection found")
        return None
        
    except Exception as e:
        print(f"❌ Local PostgreSQL test failed: {str(e)}")
        return None

def create_heroku_config():
    """Create Heroku-ready configuration"""
    print("\n🚀 Creating Heroku-ready configuration...")
    
    heroku_config = """
# Heroku Configuration
# Set these environment variables in Heroku:
# DATABASE_URL=your_heroku_postgres_url
# SECRET_KEY=your_secret_key
# JWT_SECRET_KEY=your_jwt_secret

class HerokuConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Heroku requires this for PostgreSQL
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    # Additional Heroku settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0,
        'pool_size': 10
    }
"""
    
    with open('config_heroku.py', 'w') as f:
        f.write(heroku_config)
    
    print("✅ Created config_heroku.py for Heroku deployment")

def main():
    """Main function to test connections and provide solutions"""
    print("🗄️  Database Connection Tester")
    print("=" * 50)
    
    # Test Railway connection
    railway_works = test_railway_connection()
    
    if not railway_works:
        print("\n⚠️  Railway connection failed. Testing alternatives...")
        
        # Test local PostgreSQL
        local_config = test_local_postgres()
        
        if local_config:
            print(f"\n💡 Use this local configuration: {local_config}")
            print("   Set DATABASE_URL environment variable to this value")
        else:
            print("\n💡 No PostgreSQL connection available. Options:")
            print("   1. Install PostgreSQL locally")
            print("   2. Use a cloud PostgreSQL service (Heroku Postgres, AWS RDS, etc.)")
            print("   3. Use SQLite for development (not recommended for production)")
    
    # Create Heroku configuration
    create_heroku_config()
    
    print("\n📋 Next Steps:")
    print("1. For Heroku deployment:")
    print("   - Add Heroku Postgres addon: heroku addons:create heroku-postgresql:hobby-dev")
    print("   - Set environment variables in Heroku dashboard")
    print("   - Deploy your application")
    
    print("\n2. For local development:")
    print("   - Install PostgreSQL locally")
    print("   - Create a database named 'kibtech'")
    print("   - Set DATABASE_URL environment variable")
    
    print("\n3. For Railway (if connection works):")
    print("   - The current configuration should work")
    print("   - Make sure the Railway service is running")

if __name__ == "__main__":
    main() 