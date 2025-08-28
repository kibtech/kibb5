import requests
import base64
from datetime import datetime
import json
import time

class MpesaTestFixed:
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
        
        # Configure session with better timeout and retry settings
        self.session = requests.Session()
        self.session.timeout = 30  # 30 seconds timeout
        
        # Configure retries
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def test_connectivity(self):
        """Test basic connectivity to M-Pesa API"""
        print("=== Testing Connectivity ===")
        try:
            # Test basic connection
            response = self.session.get(f"{self.base_url}", timeout=10)
            print(f"✅ Basic connectivity: Status {response.status_code}")
            return True
        except requests.exceptions.ConnectTimeout:
            print("❌ Connection timeout - check your internet connection")
            return False
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error: {e}")
            return False
        except Exception as e:
            print(f"❌ Connectivity test failed: {e}")
            return False
    
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
            
            # Use session with configured timeout and retries
            response = self.session.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers=headers,
                timeout=30
            )
            
            print(f"Access token response - Status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            if response.status_code == 200:
                token = response.json()['access_token']
                print(f"Access token: {token[:20]}...")
                return token
            else:
                raise Exception(f"Failed to get access token: {response.text}")
                
        except requests.exceptions.ConnectTimeout:
            print("❌ Connection timeout - the request took too long")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error: {e}")
            return None
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
            
            # Use session with configured timeout and retries
            response = self.session.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"STK Push API Response - Status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            return response.json()
            
        except requests.exceptions.ConnectTimeout:
            print("❌ STK Push timeout - the request took too long")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"❌ STK Push connection error: {e}")
            return None
        except Exception as e:
            print(f"STK Push error: {str(e)}")
            return None

def main():
    print("=== M-Pesa STK Push Test (Fixed) ===")
    print()
    
    # Test parameters
    phone_number = "254712591937"  # Your provided number
    amount = 1  # Test with 1 KES
    
    print(f"Testing with:")
    print(f"Phone: {phone_number}")
    print(f"Amount: {amount} KES")
    print()
    
    mpesa = MpesaTestFixed()
    
    # First test connectivity
    print("0. Testing connectivity...")
    if not mpesa.test_connectivity():
        print("❌ Connectivity test failed. Please check your internet connection.")
        print("\nTroubleshooting steps:")
        print("1. Check if you have internet access")
        print("2. Try disabling your firewall temporarily")
        print("3. Try using a mobile hotspot")
        print("4. Check if your ISP is blocking the connection")
        return
    
    print("✅ Connectivity test passed!")
    print()
    
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