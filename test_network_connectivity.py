import requests
import socket
import subprocess
import sys
import time

def test_dns_resolution():
    """Test DNS resolution for M-Pesa API"""
    print("=== DNS Resolution Test ===")
    try:
        # Test DNS resolution
        ip = socket.gethostbyname('api.safaricom.co.ke')
        print(f"✅ DNS Resolution: api.safaricom.co.ke -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS Resolution Failed: {e}")
        return False

def test_ping():
    """Test ping to M-Pesa API"""
    print("\n=== Ping Test ===")
    try:
        # Try to ping the API
        result = subprocess.run(['ping', '-n', '4', 'api.safaricom.co.ke'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ping successful")
            print(result.stdout)
        else:
            print("❌ Ping failed")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ping test error: {e}")
        return False

def test_https_connection():
    """Test HTTPS connection to M-Pesa API"""
    print("\n=== HTTPS Connection Test ===")
    try:
        # Test basic HTTPS connection
        response = requests.get('https://api.safaricom.co.ke', timeout=10)
        print(f"✅ HTTPS Connection: Status {response.status_code}")
        return True
    except requests.exceptions.ConnectTimeout:
        print("❌ HTTPS Connection: Connection timeout")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ HTTPS Connection: Connection error - {e}")
        return False
    except Exception as e:
        print(f"❌ HTTPS Connection: {e}")
        return False

def test_oauth_endpoint():
    """Test OAuth endpoint specifically"""
    print("\n=== OAuth Endpoint Test ===")
    try:
        # Test the OAuth endpoint without credentials
        response = requests.get('https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', 
                              timeout=10)
        print(f"✅ OAuth Endpoint: Status {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return True
    except requests.exceptions.ConnectTimeout:
        print("❌ OAuth Endpoint: Connection timeout")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ OAuth Endpoint: Connection error - {e}")
        return False
    except Exception as e:
        print(f"❌ OAuth Endpoint: {e}")
        return False

def test_proxy_settings():
    """Check if proxy settings are interfering"""
    print("\n=== Proxy Settings Check ===")
    
    # Check environment variables
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']
    for var in proxy_vars:
        value = requests.utils.getproxies().get(var.lower())
        if value:
            print(f"⚠️  Proxy detected: {var.lower()} = {value}")
        else:
            print(f"✅ No proxy for: {var.lower()}")
    
    # Check requests session proxies
    session = requests.Session()
    if session.proxies:
        print(f"⚠️  Session proxies: {session.proxies}")
    else:
        print("✅ No session proxies")

def test_alternative_dns():
    """Test alternative DNS servers"""
    print("\n=== Alternative DNS Test ===")
    
    # Test with Google DNS
    try:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']  # Google DNS
        answers = resolver.resolve('api.safaricom.co.ke', 'A')
        print(f"✅ Google DNS Resolution: {[str(rdata) for rdata in answers]}")
        return True
    except ImportError:
        print("⚠️  dnspython not installed, skipping DNS test")
        return False
    except Exception as e:
        print(f"❌ Google DNS Resolution failed: {e}")
        return False

def main():
    print("=== M-Pesa API Network Connectivity Test ===")
    print(f"Python version: {sys.version}")
    print(f"Requests version: {requests.__version__}")
    print()
    
    # Run all tests
    tests = [
        test_dns_resolution,
        test_ping,
        test_https_connection,
        test_oauth_endpoint,
        test_proxy_settings,
        test_alternative_dns
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n=== Summary ===")
    # Filter out None values and convert to integers
    valid_results = [1 if r else 0 for r in results if r is not None]
    passed = sum(valid_results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! Network connectivity looks good.")
    else:
        print("❌ Some tests failed. Check your network connection and firewall settings.")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Disable firewall temporarily to test")
        print("3. Try using a different network (mobile hotspot)")
        print("4. Check if your ISP is blocking the connection")
        print("5. Try using a VPN")

if __name__ == "__main__":
    main() 