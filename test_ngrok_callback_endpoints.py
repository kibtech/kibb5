#!/usr/bin/env python3
"""
Test Ngrok Callback Endpoints
This script tests if your ngrok tunnel can receive callbacks from M-Pesa
"""

import requests
import json
from datetime import datetime

# Ngrok URL
NGROK_URL = "https://f2247be98db3.ngrok-free.app"

def test_health_endpoint():
    """Test if the ngrok tunnel is accessible"""
    print("🌐 Testing ngrok tunnel accessibility...")
    
    try:
        response = requests.get(f"{NGROK_URL}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Ngrok tunnel is accessible!")
            return True
        else:
            print("⚠️ Ngrok tunnel responded but not with 200")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach ngrok tunnel: {e}")
        return False

def test_b2c_result_endpoint():
    """Test B2C result callback endpoint"""
    print(f"\n📊 Testing B2C result callback endpoint...")
    
    # Mock B2C result data
    mock_b2c_result = {
        "Result": {
            "ConversationID": "test_conversation_123",
            "ResultCode": 0,
            "ResultDesc": "The service request is processed successfully.",
            "TransactionID": "test_transaction_456",
            "ResultParameters": {
                "ResultParameter": [
                    {
                        "Key": "TransactionAmount",
                        "Value": "10"
                    },
                    {
                        "Key": "TransactionReceipt",
                        "Value": "test_receipt_789"
                    },
                    {
                        "Key": "B2CWorkingAccountAvailableFunds",
                        "Value": "1000"
                    },
                    {
                        "Key": "B2CUtilityAccountAvailableFunds",
                        "Value": "500"
                    },
                    {
                        "Key": "TransactionCompletedDateTime",
                        "Value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    },
                    {
                        "Key": "ReceiverPartyPublicName",
                        "Value": "254708541870"
                    },
                    {
                        "Key": "B2CChargesPaidAccountAvailableFunds",
                        "Value": "100"
                    }
                ]
            }
        }
    }
    
    try:
        response = requests.post(
            f"{NGROK_URL}/api/mpesa/b2c-result",
            json=mock_b2c_result,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ B2C result endpoint is working!")
            return True
        else:
            print("⚠️ B2C result endpoint responded but not with 200")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach B2C result endpoint: {e}")
        return False

def test_timeout_endpoint():
    """Test timeout callback endpoint"""
    print(f"\n⏰ Testing timeout callback endpoint...")
    
    # Mock timeout data
    mock_timeout = {
        "Result": {
            "ConversationID": "test_conversation_123",
            "ResultCode": 1,
            "ResultDesc": "The service request timed out.",
            "TransactionID": "test_transaction_456"
        }
    }
    
    try:
        response = requests.post(
            f"{NGROK_URL}/api/mpesa/timeout",
            json=mock_timeout,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Timeout endpoint is working!")
            return True
        else:
            print("⚠️ Timeout endpoint responded but not with 200")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach timeout endpoint: {e}")
        return False

def test_stk_callback_endpoint():
    """Test STK push callback endpoint"""
    print(f"\n💳 Testing STK push callback endpoint...")
    
    # Mock STK callback data
    mock_stk_callback = {
        "Body": {
            "stkCallback": {
                "MerchantRequestID": "test_merchant_request_123",
                "CheckoutRequestID": "test_checkout_request_456",
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "CallbackMetadata": {
                    "Item": [
                        {
                            "Name": "Amount",
                            "Value": 10.0
                        },
                        {
                            "Name": "MpesaReceiptNumber",
                            "Value": "test_receipt_789"
                        },
                        {
                            "Name": "TransactionDate",
                            "Value": int(datetime.now().timestamp())
                        },
                        {
                            "Name": "PhoneNumber",
                            "Value": "254708541870"
                        }
                    ]
                }
            }
        }
    }
    
    try:
        response = requests.post(
            f"{NGROK_URL}/api/mpesa/callback",
            json=mock_stk_callback,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ STK callback endpoint is working!")
            return True
        else:
            print("⚠️ STK callback endpoint responded but not with 200")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach STK callback endpoint: {e}")
        return False

def show_ngrok_instructions():
    """Show instructions for using ngrok"""
    print(f"\n📋 Ngrok Setup Instructions:")
    print("=" * 50)
    print(f"1. 🌐 Your ngrok tunnel: {NGROK_URL}")
    print(f"2. 📊 Ngrok web interface: http://localhost:4040")
    print(f"3. 🔍 Monitor requests in real-time")
    print(f"4. 📱 Test callbacks from M-Pesa")
    
    print(f"\n🔧 To start ngrok (if not running):")
    print(f"   ngrok http 5000")
    
    print(f"\n📊 To monitor callbacks:")
    print(f"   - Open http://localhost:4040 in your browser")
    print(f"   - Watch the 'HTTP' tab for incoming requests")
    print(f"   - Check your Flask app logs for processing")

def main():
    """Main test function"""
    print("🧪 Ngrok Callback Endpoints Test")
    print("=" * 50)
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print(f"\n❌ Cannot proceed - ngrok tunnel is not accessible")
        print(f"💡 Please ensure your ngrok tunnel is running")
        return False
    
    # Test callback endpoints
    b2c_ok = test_b2c_result_endpoint()
    timeout_ok = test_timeout_endpoint()
    stk_ok = test_stk_callback_endpoint()
    
    # Show instructions
    show_ngrok_instructions()
    
    # Summary
    print(f"\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    results = [
        ("Health Endpoint", health_ok),
        ("B2C Result Endpoint", b2c_ok),
        ("Timeout Endpoint", timeout_ok),
        ("STK Callback Endpoint", stk_ok)
    ]
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print(f"\n🎉 All ngrok endpoints are working correctly!")
        print(f"✅ Your system is ready to receive M-Pesa callbacks")
        print(f"🚀 You can now test B2C payments with real callbacks")
    else:
        print(f"\n⚠️ Some endpoints have issues")
        print(f"💡 Check your Flask app configuration and routes")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    print(f"\n🎯 Overall Status: {'✅ READY' if success else '❌ NEEDS FIXING'}") 