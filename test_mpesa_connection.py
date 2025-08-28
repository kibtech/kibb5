import requests
import socket
import time
import subprocess
import sys

def test_connection_with_timeout():
    """Test connection with different timeout settings"""
    print("=== Connection Timeout Test ===")
    
    timeouts = [5, 10, 15, 30]
    base_url = "https://api.safaricom.co.ke"
    
    for timeout in timeouts:
        try:
            print(f"Testing with {timeout}s timeout...")
            response = requests.get(f"{base_url}/oauth/v1/generate?grant_type=client_credentials", 
                                  timeout=timeout)
            print(f"✅ {timeout}s timeout: Status {response.status_code}")
            return True
        except requests.exceptions.ConnectTimeout:
            print(f"❌ {timeout}s timeout: Connection timeout")
        except requests.exceptions.ConnectionError as e:
            print(f"❌ {timeout}s timeout: Connection error - {e}")
        except Exception as e:
            print(f"❌ {timeout}s timeout: {e}")
    
    return False

def test_firewall_bypass():
    """Test if firewall is blocking the connection"""
    print("\n=== Firewall Bypass Test ===")
    
    # Test with different user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Python-requests/2.31.0',
        'curl/7.68.0'
    ]
    
    for ua in user_agents:
        try:
            headers = {'User-Agent': ua}
            response = requests.get('https://api.safaricom.co.ke', 
                                  headers=headers, timeout=10)
            print(f"✅ User-Agent '{ua[:20]}...': Status {response.status_code}")
        except Exception as e:
            print(f"❌ User-Agent '{ua[:20]}...': {e}")

def test_alternative_ports():
    """Test if specific ports are blocked"""
    print("\n=== Port Test ===")
    
    ports = [80, 443, 8080, 8443]
    host = "api.safaricom.co.ke"
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"✅ Port {port}: Open")
            else:
                print(f"❌ Port {port}: Closed")
            sock.close()
        except Exception as e:
            print(f"❌ Port {port}: Error - {e}")

def test_curl_equivalent():
    """Test using curl-like approach"""
    print("\n=== Curl Equivalent Test ===")
    
    try:
        # Use requests with curl-like settings
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'curl/7.68.0',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        })
        
        response = session.get('https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
                             timeout=15)
        print(f"✅ Curl equivalent: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Curl equivalent: {e}")
        return False

def test_windows_firewall():
    """Check Windows Firewall status"""
    print("\n=== Windows Firewall Check ===")
    
    try:
        # Check firewall status
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            output = result.stdout
            if "ON" in output:
                print("⚠️  Windows Firewall is ON - this might be blocking the connection")
                print("   Try: netsh advfirewall set allprofiles state off")
            else:
                print("✅ Windows Firewall appears to be OFF")
        else:
            print("❌ Could not check firewall status")
            
    except Exception as e:
        print(f"❌ Firewall check error: {e}")

def test_network_adapters():
    """Check network adapter settings"""
    print("\n=== Network Adapter Check ===")
    
    try:
        result = subprocess.run(['ipconfig', '/all'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            output = result.stdout
            if "DNS Servers" in output:
                print("✅ DNS servers configured")
                # Extract DNS servers
                lines = output.split('\n')
                for line in lines:
                    if "DNS Servers" in line:
                        print(f"   {line.strip()}")
            else:
                print("❌ No DNS servers found")
        else:
            print("❌ Could not check network adapters")
            
    except Exception as e:
        print(f"❌ Network adapter check error: {e}")

def main():
    print("=== M-Pesa Connection Diagnostic ===")
    print("Based on your test results, the issue appears to be firewall/network related.")
    print("Let's run targeted tests to identify the exact problem.\n")
    
    tests = [
        test_connection_with_timeout,
        test_firewall_bypass,
        test_alternative_ports,
        test_curl_equivalent,
        test_windows_firewall,
        test_network_adapters
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n=== Recommended Solutions ===")
    print("Based on the test results, try these solutions in order:")
    print()
    print("1. TEMPORARILY disable Windows Firewall:")
    print("   - Open Windows Security")
    print("   - Go to Firewall & network protection")
    print("   - Turn off Windows Defender Firewall")
    print("   - Test STK push")
    print("   - Re-enable if it works")
    print()
    print("2. If firewall doesn't help, try mobile hotspot:")
    print("   - Use your phone's mobile data")
    print("   - Test STK push from mobile network")
    print()
    print("3. Check antivirus software:")
    print("   - Temporarily disable real-time protection")
    print("   - Test STK push")
    print("   - Re-enable if it works")
    print()
    print("4. Try different DNS servers:")
    print("   - Change to Google DNS: 8.8.8.8, 8.8.4.4")
    print("   - Or Cloudflare DNS: 1.1.1.1, 1.0.0.1")
    print()
    print("5. If all else fails, use a VPN service")

if __name__ == "__main__":
    main() 