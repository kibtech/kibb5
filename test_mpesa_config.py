#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_mpesa_config():
    """Test M-Pesa configuration and see what's happening"""
    print("1. Testing M-Pesa configuration...")
    
    try:
        # Test the M-Pesa config endpoint
        config_response = requests.get(f'{BASE_URL}/api/mpesa/test-config')
        print(f"Config test status: {config_response.status_code}")
        print(f"Config response: {config_response.text}")
        
        print("\n2. Testing M-Pesa debug config...")
        debug_response = requests.get(f'{BASE_URL}/api/mpesa/debug-config')
        print(f"Debug config status: {debug_response.status_code}")
        print(f"Debug config response: {debug_response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_mpesa_config() 