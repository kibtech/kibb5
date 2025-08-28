#!/usr/bin/env python3
"""
Fix DNS Resolution for M-Pesa API
=================================
This script helps diagnose and fix DNS resolution issues.
"""

import socket
import subprocess
import requests
import sys
import os

def test_basic_connectivity():
    """Test basic internet connectivity"""
    print("=== Basic Internet Connectivity Test ===")
    
    # Test with a known working domain
    try:
        ip = socket.gethostbyname('google.com')
        print(f"✅ Google DNS: google.com -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ Google DNS failed: {e}")
        return False

def test_safaricom_dns():
    """Test Safaricom DNS resolution"""
    print("\n=== Safaricom DNS Test ===")
    
    try:
        ip = socket.gethostbyname('api.safaricom.co.ke')
        print(f"✅ Safaricom DNS: api.safaricom.co.ke -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ Safaricom DNS failed: {e}")
        return False

def test_with_google_dns():
    """Test using Google DNS servers"""
    print("\n=== Testing with Google DNS ===")
    
    try:
        # Create a resolver with Google DNS
            resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            resolver.settimeout(5)
            
        # Try to connect to Google DNS
        resolver.connect(('8.8.8.8', 53))
        print("✅ Can reach Google DNS (8.8.8.8)")
        
        # Try to resolve using nslookup with Google DNS
        try:
            result = subprocess.run(
                ['nslookup', 'api.safaricom.co.ke', '8.8.8.8'], 
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print("✅ nslookup with Google DNS successful")
                print(result.stdout)
                return True
            else:
                print("❌ nslookup with Google DNS failed")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ nslookup error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot reach Google DNS: {e}")
        return False

def test_alternative_domains():
    """Test alternative Safaricom domains"""
    print("\n=== Testing Alternative Domains ===")
    
    domains = [
        'safaricom.co.ke',
        'www.safaricom.co.ke',
        'api.safaricom.com',
        'sandbox.safaricom.co.ke'
    ]
    
    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)
            print(f"✅ {domain} -> {ip}")
        except socket.gaierror as e:
            print(f"❌ {domain} -> {e}")

def flush_dns_cache():
    """Flush DNS cache on Windows"""
    print("\n=== Flushing DNS Cache ===")
    
    try:
        result = subprocess.run(['ipconfig', '/flushdns'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ DNS cache flushed successfully")
            return True
        else:
            print("❌ Failed to flush DNS cache")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error flushing DNS cache: {e}")
        return False

def test_with_requests():
    """Test with requests library using different DNS"""
    print("\n=== Testing with Requests ===")
    
    # Test with a working domain first
    try:
        response = requests.get('https://httpbin.org/ip', timeout=10)
        print(f"✅ Internet connectivity: {response.json()}")
        except Exception as e:
        print(f"❌ Internet connectivity failed: {e}")
        return False
    
    # Test Safaricom API
    try:
        response = requests.get('https://api.safaricom.co.ke', timeout=10)
        print(f"✅ Safaricom API accessible: Status {response.status_code}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Safaricom API connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Safaricom API error: {e}")
        return False

def suggest_solutions():
    """Suggest solutions based on test results"""
    print("\n=== Suggested Solutions ===")
    print("1. Try using a mobile hotspot to test if it's a network issue")
    print("2. Disable Windows Firewall temporarily")
    print("3. Try using a VPN")
    print("4. Check if your ISP is blocking the connection")
    print("5. Try changing your DNS servers to Google DNS (8.8.8.8, 8.8.4.4)")
    print("6. Restart your router/modem")
    print("7. Try from a different network")

def main():
    print("=== DNS Resolution Fix for M-Pesa API ===")
    print()
    
    # Run tests
    tests = [
        test_basic_connectivity,
        test_safaricom_dns,
        test_with_google_dns,
        test_alternative_domains,
        flush_dns_cache,
        test_with_requests
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
    
    print("\n=== Summary ===")
    passed = sum([1 for r in results if r])
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! DNS resolution should work now.")
    else:
        print("❌ Some tests failed. DNS resolution issues detected.")
        suggest_solutions()

if __name__ == "__main__":
    main() 