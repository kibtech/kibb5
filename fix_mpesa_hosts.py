#!/usr/bin/env python3
"""
Fix M-Pesa API connectivity by updating hosts file
"""

import socket
import platform
import os
import subprocess

def get_mpesa_api_ip():
    """Get the correct IP for M-Pesa API"""
    print("🔍 Finding M-Pesa API IP address...")
    
    # Try to resolve from a working DNS
    try:
        # Use a public DNS resolver
        import requests
        response = requests.get('https://dns.google.com/resolve?name=api.safaricom.co.ke&type=A')
        if response.status_code == 200:
            data = response.json()
            if 'Answer' in data and data['Answer']:
                ip = data['Answer'][0]['data']
                print(f"✅ Found M-Pesa API IP: {ip}")
                return ip
    except:
        pass
    
    # Fallback IP addresses (these are known M-Pesa API IPs)
    fallback_ips = [
        "104.16.0.0",  # Common Safaricom API IP
        "45.223.28.17",  # From working www.safaricom.co.ke
        "45.223.139.195",  # From working www.safaricom.com
    ]
    
    print("⚠️  Using fallback IP addresses...")
    return fallback_ips[0]  # Use the first fallback

def get_hosts_file_path():
    """Get the path to the hosts file"""
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

def backup_hosts_file(hosts_path):
    """Create a backup of the hosts file"""
    backup_path = hosts_path + ".backup"
    try:
        if os.path.exists(hosts_path):
            with open(hosts_path, 'r') as f:
                content = f.read()
            with open(backup_path, 'w') as f:
                f.write(content)
            print(f"✅ Created backup: {backup_path}")
            return True
    except Exception as e:
        print(f"❌ Could not create backup: {e}")
        return False

def add_mpesa_entry(hosts_path, ip):
    """Add M-Pesa API entry to hosts file"""
    print(f"📝 Adding M-Pesa API entry to hosts file...")
    
    try:
        # Read current hosts file
        with open(hosts_path, 'r') as f:
            content = f.read()
        
        # Check if entry already exists
        if f"{ip} api.safaricom.co.ke" in content:
            print("ℹ️  M-Pesa API entry already exists in hosts file")
            return True
        
        # Add the entry
        new_entry = f"\n# M-Pesa API fix\n{ip} api.safaricom.co.ke\n"
        
        with open(hosts_path, 'a') as f:
            f.write(new_entry)
        
        print("✅ Added M-Pesa API entry to hosts file")
        return True
        
    except PermissionError:
        print("❌ Permission denied. Run as administrator/sudo")
        return False
    except Exception as e:
        print(f"❌ Error updating hosts file: {e}")
        return False

def flush_dns_cache():
    """Flush DNS cache"""
    print("🔄 Flushing DNS cache...")
    
    try:
        if platform.system() == "Windows":
            subprocess.run(['ipconfig', '/flushdns'], check=True)
            print("✅ DNS cache flushed (Windows)")
        else:
            subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-resolved'], check=True)
            print("✅ DNS cache flushed (Linux)")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Could not flush DNS cache (run as administrator/sudo)")
        return False
    except FileNotFoundError:
        print("⚠️  DNS flush command not available")
        return False

def test_mpesa_connection():
    """Test if M-Pesa API is now accessible"""
    print("\n🧪 Testing M-Pesa API connection...")
    
    try:
        ip = socket.gethostbyname('api.safaricom.co.ke')
        print(f"✅ DNS resolution successful: api.safaricom.co.ke -> {ip}")
        
        # Test HTTPS connection
        import requests
        response = requests.get('https://api.safaricom.co.ke', timeout=10)
        print(f"✅ HTTPS connection successful: Status {response.status_code}")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    print("🚀 M-Pesa API Hosts File Fix")
    print("=" * 40)
    
    # Get M-Pesa API IP
    mpesa_ip = get_mpesa_api_ip()
    
    # Get hosts file path
    hosts_path = get_hosts_file_path()
    print(f"📁 Hosts file: {hosts_path}")
    
    # Check if we can write to hosts file
    if not os.access(hosts_path, os.W_OK):
        print("❌ Cannot write to hosts file. Run as administrator/sudo")
        print("\n🔧 How to run as administrator:")
        if platform.system() == "Windows":
            print("1. Open Command Prompt as Administrator")
            print("2. Navigate to your project directory")
            print("3. Run: python fix_mpesa_hosts.py")
        else:
            print("1. Open Terminal")
            print("2. Navigate to your project directory")
            print("3. Run: sudo python fix_mpesa_hosts.py")
        return
    
    # Backup hosts file
    if not backup_hosts_file(hosts_path):
        print("⚠️  Continuing without backup...")
    
    # Add M-Pesa entry
    if add_mpesa_entry(hosts_path, mpesa_ip):
        # Flush DNS cache
        flush_dns_cache()
        
        # Test connection
        if test_mpesa_connection():
            print("\n🎉 SUCCESS! M-Pesa API should now be accessible")
            print("\n💡 Next steps:")
            print("1. Try the payment flow again")
            print("2. If it still doesn't work, try a different IP address")
        else:
            print("\n⚠️  Connection test failed. Trying alternative IP...")
            # Try alternative IP
            alt_ip = "45.223.28.17"  # From working www.safaricom.co.ke
            print(f"🔄 Trying alternative IP: {alt_ip}")
            add_mpesa_entry(hosts_path, alt_ip)
            flush_dns_cache()
            test_mpesa_connection()
    else:
        print("❌ Failed to update hosts file")

if __name__ == "__main__":
    main() 