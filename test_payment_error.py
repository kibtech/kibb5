#!/usr/bin/env python3
"""
Test payment endpoint to see the specific error
"""

import requests
import json

def test_payment_error():
    # Test the payment endpoint with the order number from the logs
    order_number = "CS202508031117226"
    
    # You'll need to get a valid token first
    print("Testing payment endpoint...")
    print(f"Order Number: {order_number}")
    
    # This is a test to see what the error response looks like
    # You'll need to run this with a valid token
    url = f"http://localhost:5000/api/cyber-services/orders/{order_number}/pay"
    
    print(f"URL: {url}")
    print("Note: You need to run this with a valid authentication token")
    print("The 400 error suggests either:")
    print("1. Invalid phone number format")
    print("2. Invalid amount")
    print("3. Missing M-Pesa configuration")
    print("4. User phone number not found")

if __name__ == "__main__":
    test_payment_error() 