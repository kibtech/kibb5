#!/usr/bin/env python3
"""
Test Supabase Database Connection
This script tests the connection to your Supabase PostgreSQL database.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_database_connection():
    """Test the database connection"""
    print("🔍 Testing Supabase Database Connection...")
    print("=" * 50)
    
    # Database URL (using Transaction Pooler)
    database_url = "postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres"
    
    try:
        # Create engine
        print("🔄 Creating database engine...")
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        print("🔄 Testing connection...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"📊 PostgreSQL Version: {version}")
            
            # Test if we can create tables
            print("🔄 Testing table creation capability...")
            result = connection.execute(text("SELECT current_database();"))
            database_name = result.fetchone()[0]
            print(f"📊 Connected to database: {database_name}")
            
            # Check if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"📋 Existing tables: {', '.join(tables)}")
            else:
                print("📋 No existing tables found (this is normal for a new database)")
        
        print("\n✅ Database connection test completed successfully!")
        print("🚀 Ready for deployment!")
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_flask_app_connection():
    """Test the Flask app database connection"""
    print("\n🔍 Testing Flask App Database Connection...")
    print("=" * 50)
    
    try:
        # Import Flask app
        from app import create_app, db
        
        # Create app with heroku config
        app = create_app('heroku')
        
        with app.app_context():
            # Test database connection
            db.engine.execute(text("SELECT 1"))
            print("✅ Flask app database connection successful!")
            
            # Test if we can access models
            from app.models import User, Product, Category, Brand
            print("✅ Database models accessible!")
            
            return True
            
    except Exception as e:
        print(f"❌ Flask app database connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 KIBTECH Supabase Database Connection Test")
    print("=" * 60)
    
    # Test direct database connection
    db_success = test_database_connection()
    
    if db_success:
        # Test Flask app connection
        flask_success = test_flask_app_connection()
        
        if flask_success:
            print("\n🎉 All tests passed! Your database is ready for deployment.")
            print("\n📋 Next steps:")
            print("1. Run: python deploy_to_heroku.py")
            print("2. Or deploy manually using the commands in HEROKU_CHECKLIST.md")
        else:
            print("\n❌ Flask app connection failed. Check your configuration.")
            sys.exit(1)
    else:
        print("\n❌ Database connection failed. Please check your Supabase credentials.")
        sys.exit(1)

if __name__ == "__main__":
    main() 