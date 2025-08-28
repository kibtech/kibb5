import requests
import base64
from datetime import datetime
import json

class WithdrawalTest:
    def __init__(self):
        # Production credentials
        self.consumer_key = "3yOAC0yXFibCzvMQz4hh0ORIDcM1ai947hI1Rt0Fe3yYj5L5"
        self.consumer_secret = "ptg1TQDPaKNiIVWhpxMYDk8NAPiFMGiA062Nt7EGGovsNxuZeFTHPXgwgE4umWJf"
        self.shortcode = "3547179"
        self.base_url = "https://api.safaricom.co.ke"
        
        # Production passkey
        self.passkey = "e0232ed3a06890a62b026b48a7c9ba25e1217825a76312907a1c3cfaffb48856"
        
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
    
    def test_b2c_endpoint(self, phone_number, amount):
        """Test B2C withdrawal endpoint"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return None
            
            print(f"B2C Withdrawal - Token: {access_token[:20]}...")
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Note: B2C requires initiator name and security credential
            # This is a test to see if the endpoint is accessible
            payload = {
                "InitiatorName": "testapi",  # This would need to be configured
                "SecurityCredential": "test",  # This would need proper encryption
                "CommandID": "BusinessPayment",
                "Amount": int(amount),
                "PartyA": self.shortcode,
                "PartyB": phone_number,
                "Remarks": "Test withdrawal",
                            "QueueTimeOutURL": "https://kibtech.co.ke/api/mpesa/timeout",
            "ResultURL": "https://kibtech.co.ke/api/mpesa/b2c-result",
                "Occasion": "Test"
            }
            
            print(f"B2C payload: {json.dumps(payload, indent=2)}")
            
            response = self.session.post(
                f"{self.base_url}/mpesa/b2c/v1/paymentrequest",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"B2C API Response - Status: {response.status_code}")
            print(f"Response body: {response.text}")
            
            return response.json()
            
        except requests.exceptions.ConnectTimeout:
            print("❌ B2C timeout - the request took too long")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"❌ B2C connection error: {e}")
            return None
        except Exception as e:
            print(f"B2C error: {str(e)}")
            return None

def main():
    print("=== M-Pesa B2C Withdrawal Test ===")
    print()
    
    # Test parameters
    phone_number = "254712591937"  # Your provided number
    amount = 1  # Test with 1 KES
    
    print(f"Testing with:")
    print(f"Phone: {phone_number}")
    print(f"Amount: {amount} KES")
    print()
    
    withdrawal = WithdrawalTest()
    
    print("1. Getting access token...")
    token = withdrawal.get_access_token()
    
    if token:
        print("✅ Access token obtained successfully!")
        print()
        
        print("2. Testing B2C endpoint...")
        print("Note: This will likely fail with authentication errors because")
        print("B2C requires proper initiator name and security credential configuration.")
        print("This test is to verify the endpoint is accessible.\n")
        
        result = withdrawal.test_b2c_endpoint(phone_number, amount)
        
        if result:
            if 'ConversationID' in result:
                print("✅ B2C withdrawal initiated successfully!")
                print(f"ConversationID: {result['ConversationID']}")
                print(f"OriginatorConversationID: {result['OriginatorConversationID']}")
                print(f"ResponseCode: {result['ResponseCode']}")
                print(f"ResponseDescription: {result['ResponseDescription']}")
            elif 'errorCode' in result:
                print("❌ B2C failed with error:")
                print(f"Error Code: {result.get('errorCode')}")
                print(f"Error Message: {result.get('errorMessage')}")
                print("\nThis is expected if initiator credentials are not configured.")
            else:
                print("❌ B2C failed!")
                print(f"Response: {result}")
        else:
            print("❌ B2C failed!")
    else:
        print("❌ Failed to get access token!")

if __name__ == "__main__":
    main() 