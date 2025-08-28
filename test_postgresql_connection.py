#!/usr/bin/env python3
"""
Test PostgreSQL Connection and Troubleshooting
=============================================

This script tests the PostgreSQL connection to Railway and provides
troubleshooting steps if the connection fails.
"""

import sys
import os
import socket
import time
import psycopg2
from urllib.parse import urlparse

def test_network_connectivity(host, port):
    """Test basic network connectivity to the database host"""
    print(f"🔍 Testing network connectivity to {host}:{port}...")
    
    try:
        # Test socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ Network connectivity successful!")
            return True
        else:
            print(f"❌ Network connectivity failed (error code: {result})")
            return False
            
    except Exception as e:
        print(f"❌ Network connectivity test failed: {str(e)}")
        return False

def test_postgresql_connection():
    """Test PostgreSQL connection to Railway"""
    print("🔍 Testing PostgreSQL connection to Railway...")
    
    # Parse the connection string
    connection_string = "postgresql://postgres:UyAUrqMDtsFssWrwYdYRaqNfNMFpNbqW@trolley.proxy.rlwy.net:20673/railway"
    
    try:
        # Test connection
        conn = psycopg2.connect(connection_string, connect_timeout=10)
        cursor = conn.cursor()
        
        # Test a simple query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print("✅ PostgreSQL connection successful!")
        print(f"📊 Database version: {version[0]}")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def check_railway_status():
    """Check if Railway service is accessible"""
    print("🔍 Checking Railway service status...")
    
    # Test multiple Railway endpoints
    railway_hosts = [
        ("trolley.proxy.rlwy.net", 20673),
        ("railway.app", 443),
        ("api.railway.app", 443)
    ]
    
    for host, port in railway_hosts:
        print(f"   Testing {host}:{port}...")
        if test_network_connectivity(host, port):
            print(f"   ✅ {host}:{port} is accessible")
        else:
            print(f"   ❌ {host}:{port} is not accessible")

def provide_troubleshooting_steps():
    """Provide troubleshooting steps for PostgreSQL connection issues"""
    print("\n🔧 Troubleshooting Steps:")
    print("=" * 50)
    
    print("1. 🌐 Check Internet Connection:")
    print("   - Ensure you have a stable internet connection")
    print("   - Try accessing other websites to confirm connectivity")
    
    print("\n2. 🔥 Check Firewall Settings:")
    print("   - Ensure your firewall allows outbound connections to port 20673")
    print("   - Check if your antivirus is blocking the connection")
    
    print("\n3. 🚄 Railway Service Status:")
    print("   - Visit https://status.railway.app to check service status")
    print("   - Railway PostgreSQL might be experiencing downtime")
    
    print("\n4. 🔑 Verify Database Credentials:")
    print("   - Check if the database credentials are still valid")
    print("   - Railway might have rotated the credentials")
    
    print("\n5. 🌍 Network Restrictions:")
    print("   - Some networks (corporate, school) block certain ports")
    print("   - Try connecting from a different network")
    
    print("\n6. 🔄 Alternative Solutions:")
    print("   - Use a different Railway region")
    print("   - Set up a local PostgreSQL database for development")
    print("   - Use a different cloud database provider")

def test_alternative_connection_methods():
    """Test alternative connection methods"""
    print("\n🔄 Testing Alternative Connection Methods:")
    print("=" * 50)
    
    # Test with different connection parameters
    connection_variants = [
        {
            "name": "Standard Connection",
            "params": {
                "host": "trolley.proxy.rlwy.net",
                "port": 20673,
                "database": "railway",
                "user": "postgres",
                "password": "UyAUrqMDtsFssWrwYdYRaqNfNMFpNbqW",
                "connect_timeout": 10
            }
        },
        {
            "name": "Connection with SSL",
            "params": {
                "host": "trolley.proxy.rlwy.net",
                "port": 20673,
                "database": "railway",
                "user": "postgres",
                "password": "UyAUrqMDtsFssWrwYdYRaqNfNMFpNbqW",
                "connect_timeout": 10,
                "sslmode": "require"
            }
        }
    ]
    
    for variant in connection_variants:
        print(f"\n📡 Testing {variant['name']}...")
        try:
            conn = psycopg2.connect(**variant['params'])
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
            conn.close()
            print(f"✅ {variant['name']} successful!")
        except Exception as e:
            print(f"❌ {variant['name']} failed: {str(e)}")

def main():
    """Main function to test PostgreSQL connection"""
    print("🚀 PostgreSQL Connection Test Tool")
    print("=" * 50)
    
    # Test network connectivity first
    if not test_network_connectivity("trolley.proxy.rlwy.net", 20673):
        print("\n❌ Network connectivity failed. This might be a network issue.")
        check_railway_status()
        provide_troubleshooting_steps()
        return False
    
    # Test PostgreSQL connection
    if not test_postgresql_connection():
        print("\n❌ PostgreSQL connection failed. Testing alternatives...")
        test_alternative_connection_methods()
        provide_troubleshooting_steps()
        return False
    
    print("\n✅ All tests passed! PostgreSQL connection is working.")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💡 If the connection continues to fail, consider:")
        print("   - Contacting Railway support")
        print("   - Using a different database provider")
        print("   - Setting up a local PostgreSQL for development")
        sys.exit(1) 