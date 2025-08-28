#!/usr/bin/env python3
"""
Test M-Pesa API connectivity
"""

import requests
import socket
import subprocess
import sys
import os

def test_dns_resolution():
    """Test if we can resolve the M-Pesa API domain"""
    print("🔍 Testing DNS resolution...")
    try:
        ip = socket.gethostbyname('api.safaricom.co.ke')
        print(f"✅ DNS resolution successful: api.safaricom.co.ke -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        return False

def test_ping():
    """Test ping to M-Pesa API server"""
    print("\n🏓 Testing ping connectivity...")
    try:
        result = subprocess.run(['ping', '-c', '3', 'api.safaricom.co.ke'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ping successful")
            return True
        else:
            print(f"❌ Ping failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Ping timeout")
        return False
    except FileNotFoundError:
        print("⚠️  Ping command not available (Windows)")
        return None

def test_https_connection():
    """Test HTTPS connection to M-Pesa API"""
    print("\n🌐 Testing HTTPS connection...")
    try:
        response = requests.get('https://api.safaricom.co.ke', timeout=10)
        print(f"✅ HTTPS connection successful: Status {response.status_code}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"❌ HTTPS connection failed: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"❌ HTTPS connection timeout: {e}")
        return False
    except Exception as e:
        print(f"❌ HTTPS connection error: {e}")
        return False

def test_oauth_endpoint():
    """Test the OAuth endpoint specifically"""
    print("\n🔐 Testing OAuth endpoint...")
    try:
        response = requests.get('https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', 
                              timeout=10)
        print(f"✅ OAuth endpoint accessible: Status {response.status_code}")
        if response.status_code == 401:
            print("ℹ️  Expected 401 (Unauthorized) - this means the endpoint is reachable but needs credentials")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"❌ OAuth endpoint connection failed: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"❌ OAuth endpoint timeout: {e}")
        return False
    except Exception as e:
        print(f"❌ OAuth endpoint error: {e}")
        return False

def check_environment():
    """Check environment variables and configuration"""
    print("\n⚙️  Checking environment...")
    
    # Check if we're in a development environment
    if os.getenv('FLASK_ENV') == 'development':
        print("ℹ️  Running in development mode")
    
    # Check proxy settings
    http_proxy = os.getenv('HTTP_PROXY') or os.getenv('http_proxy')
    https_proxy = os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')
    
    if http_proxy:
        print(f"ℹ️  HTTP Proxy configured: {http_proxy}")
    if https_proxy:
        print(f"ℹ️  HTTPS Proxy configured: {https_proxy}")
    
    if not http_proxy and not https_proxy:
        print("ℹ️  No proxy configured")

def main():
    print("🚀 M-Pesa API Connectivity Test")
    print("=" * 40)
    
    # Test DNS resolution
    dns_ok = test_dns_resolution()
    
    # Test ping (if available)
    ping_ok = test_ping()
    
    # Test HTTPS connection
    https_ok = test_https_connection()
    
    # Test OAuth endpoint
    oauth_ok = test_oauth_endpoint()
    
    # Check environment
    check_environment()
    
    print("\n" + "=" * 40)
    print("📊 SUMMARY:")
    print(f"DNS Resolution: {'✅ OK' if dns_ok else '❌ FAILED'}")
    print(f"Ping: {'✅ OK' if ping_ok else '❌ FAILED' if ping_ok is False else '⚠️  NOT TESTED'}")
    print(f"HTTPS Connection: {'✅ OK' if https_ok else '❌ FAILED'}")
    print(f"OAuth Endpoint: {'✅ OK' if oauth_ok else '❌ FAILED'}")
    
    if not dns_ok:
        print("\n🔧 TROUBLESHOOTING SUGGESTIONS:")
        print("1. Check your internet connection")
        print("2. Try using a different DNS server (e.g., 8.8.8.8 or 1.1.1.1)")
        print("3. Check if you're behind a corporate firewall")
        print("4. Try using a VPN if you're in a restricted network")
        print("5. Check your hosts file for any conflicting entries")
    
    if dns_ok and not https_ok:
        print("\n🔧 TROUBLESHOOTING SUGGESTIONS:")
        print("1. Check your firewall settings")
        print("2. Try disabling antivirus temporarily")
        print("3. Check if you need to configure a proxy")
        print("4. Try using a different network connection")

if __name__ == "__main__":
    main() 