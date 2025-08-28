import requests
import base64
from datetime import datetime
import json

class MpesaTest:
    def __init__(self):
        # Production credentials
        self.consumer_key = "3yOAC0yXFibCzvMQz4hh0ORIDcM1ai947hI1Rt0Fe3yYj5L5"
        self.consumer_secret = "ptg1TQDPaKNiIVWhpxMYDk8NAPiFMGiA062Nt7EGGovsNxuZeFTHPXgwgE4umWJf"
        self.shortcode = "3547179"
        self.base_url = "https://api.safaricom.co.ke"
        
        # Production passkey
        self.passkey = "e0232ed3a06890a62b026b48a7c9ba25e1217825a76312907a1c3cfaffb48856"
        
        # Test callback URL (replace with your actual callback URL)
        self.callback_url = "https://your-domain.com/api/mpesa/callback"
    
    def get_access_token(self):
        """Get OAuth access token from Daraja API"""
        try:
            # Encode credentials
            credentials = f"{self.consumer_key}:{self.consumer_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            print(f"Getting access token from: {self.base_url}")
            print(f"Consumer Key: {self.consumer_key[:10]}...")
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers=headers
            )
            
            print(f"Access token response - Status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            if response.status_code == 200:
                token = response.json()['access_token']
                print(f"Access token: {token[:20]}...")
                return token
            else:
                raise Exception(f"Failed to get access token: {response.text}")
                
        except Exception as e:
            print(f"Access token error: {str(e)}")
            return None
    
    def generate_password(self):
        """Generate password for STK Push"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        return password, timestamp
    
    def stk_push(self, phone_number, amount):
        """Initiate STK Push payment"""
        try:
            # Check if passkey is set
            if self.passkey == "YOUR_PASSKEY_HERE":
                print("ERROR: Please set your passkey in the script!")
                return None
            
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            password, timestamp = self.generate_password()
            
            print(f"STK Push - Token: {access_token[:20]}..., Password: {password[:20]}..., Timestamp: {timestamp}")
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": self.callback_url,
                "AccountReference": "TestPayment",
                "TransactionDesc": "Test STK Push"
            }
            
            print(f"STK Push payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers
            )
            
            print(f"STK Push API Response - Status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            return response.json()
            
        except Exception as e:
            print(f"STK Push error: {str(e)}")
            return None

def main():
    print("=== M-Pesa STK Push Test ===")
    print()
    
    # Test parameters
    phone_number = "254712591937"  # Your provided number
    amount = 1  # Test with 1 KES
    
    print(f"Testing with:")
    print(f"Phone: {phone_number}")
    print(f"Amount: {amount} KES")
    print()
    
    mpesa = MpesaTest()
    
    print("1. Getting access token...")
    token = mpesa.get_access_token()
    
    if token:
        print("✅ Access token obtained successfully!")
        print()
        
        print("2. Initiating STK Push...")
        result = mpesa.stk_push(phone_number, amount)
        
        if result:
            if 'CheckoutRequestID' in result:
                print("✅ STK Push initiated successfully!")
                print(f"CheckoutRequestID: {result['CheckoutRequestID']}")
                print(f"MerchantRequestID: {result['MerchantRequestID']}")
                print(f"ResponseCode: {result['ResponseCode']}")
                print(f"ResponseDescription: {result['ResponseDescription']}")
            else:
                print("❌ STK Push failed!")
                print(f"Error: {result}")
        else:
            print("❌ STK Push failed!")
    else:
        print("❌ Failed to get access token!")

if __name__ == "__main__":
    main() 