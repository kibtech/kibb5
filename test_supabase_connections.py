#!/usr/bin/env python3
"""
Test Different Supabase Connection Formats
This script tests various connection string formats to find the correct one.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_connection(database_url, description):
    """Test a specific database connection"""
    print(f"\n🔍 Testing: {description}")
    print(f"URL: {database_url}")
    print("-" * 50)
    
    try:
        # Create engine
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ SUCCESS! PostgreSQL Version: {version}")
            
            # Test database name
            result = connection.execute(text("SELECT current_database();"))
            database_name = result.fetchone()[0]
            print(f"📊 Connected to database: {database_name}")
            
            return True
            
    except SQLAlchemyError as e:
        print(f"❌ FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return False

def main():
    """Test different connection formats"""
    print("🚀 KIBTECH Supabase Connection String Test")
    print("=" * 60)
    
    # Test different connection formats
    connections = [
        {
            "url": "postgresql://postgres:Kibtech@db.fcrvabkgdhdvprwwlyuf.supabase.co:5432/postgres",
            "description": "Direct Connection (Original)"
        },
        {
            "url": "postgresql://postgres:Kibtech@db.fcrvabkgdhdvprwwlyuf.supabase.co:5432/postgres",
            "description": "Direct Connection (Corrected hostname)"
        },
        {
            "url": "postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres",
            "description": "Transaction Pooler"
        },
        {
            "url": "postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:5432/postgres",
            "description": "Session Pooler"
        }
    ]
    
    successful_connections = []
    
    for conn in connections:
        if test_connection(conn["url"], conn["description"]):
            successful_connections.append(conn)
    
    print("\n" + "=" * 60)
    print("📋 RESULTS SUMMARY")
    print("=" * 60)
    
    if successful_connections:
        print(f"✅ {len(successful_connections)} successful connection(s) found:")
        for i, conn in enumerate(successful_connections, 1):
            print(f"{i}. {conn['description']}")
            print(f"   URL: {conn['url']}")
        
        print("\n🎉 Use the first successful connection for your deployment!")
        
        # Update the configuration with the first successful connection
        if successful_connections:
            best_connection = successful_connections[0]
            print(f"\n📝 Recommended connection string:")
            print(f"   {best_connection['url']}")
            
    else:
        print("❌ No successful connections found.")
        print("Please check your Supabase credentials and network connectivity.")
        sys.exit(1)

if __name__ == "__main__":
    main() 