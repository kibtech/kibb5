# M-Pesa STK Push Troubleshooting Guide

## Issue Summary
The STK push is failing due to network connectivity issues:
- **Name Resolution Error**: `Failed to resolve 'api.safaricom.co.ke'`
- **Connection Timeout**: `Connection to api.safaricom.co.ke timed out`

## Root Cause
The problem is **network connectivity** - your system cannot reach the M-Pesa API servers at `api.safaricom.co.ke`.

## Diagnostic Tests

### 1. Run Network Connectivity Test
```bash
python test_network_connectivity.py
```

This will test:
- DNS resolution
- Ping connectivity
- HTTPS connection
- OAuth endpoint accessibility
- Proxy settings
- Alternative DNS servers

### 2. Run Improved STK Push Test
```bash
python test_stk_push_fixed.py
```

This includes:
- Better timeout settings (30 seconds)
- Automatic retries
- Connectivity testing before attempting STK push
- Detailed error messages

## Troubleshooting Steps

### Step 1: Check Internet Connection
1. Open a web browser and try to access any website
2. If you can't browse, fix your internet connection first

### Step 2: Test DNS Resolution
```bash
nslookup api.safaricom.co.ke
```
Expected output:
```
Name:    api.safaricom.co.ke
Address:  [some IP address]
```

### Step 3: Test Ping
```bash
ping api.safaricom.co.ke
```
If ping fails, try:
```bash
ping 8.8.8.8
```
If 8.8.8.8 works but api.safaricom.co.ke doesn't, it's a DNS issue.

### Step 4: Check Firewall Settings
1. **Windows Firewall**: Temporarily disable to test
   - Open Windows Security → Firewall & network protection
   - Turn off Windows Defender Firewall temporarily
   - Test STK push
   - Re-enable if it works

2. **Antivirus Software**: Check if your antivirus is blocking the connection
   - Temporarily disable real-time protection
   - Test STK push
   - Re-enable if it works

### Step 5: Try Different Network
1. **Mobile Hotspot**: Use your phone's mobile data
2. **Different WiFi**: Try a different network
3. **VPN**: Try using a VPN service

### Step 6: Check Proxy Settings
If you're on a corporate network:
1. Check if proxy is required
2. Configure proxy settings in your environment
3. Or try from a non-corporate network

### Step 7: Alternative DNS Servers
Try using Google DNS:
1. Open Network Settings
2. Change DNS to 8.8.8.8 and 8.8.4.4
3. Test again

## Quick Fixes

### Fix 1: Update MPESA Service (Already Done)
The MPESA service has been updated with:
- Better timeout settings (30 seconds)
- Automatic retries
- Improved error handling
- Connection testing

### Fix 2: Environment Variables
Make sure these are set correctly:
```bash
MPESA_BASE_URL=https://api.safaricom.co.ke
MPESA_CONSUMER_KEY=3yOAC0yXFibCzvMQz4hh0ORIDcM1ai947hI1Rt0Fe3yYj5L5
MPESA_CONSUMER_SECRET=ptg1TQDPaKNiIVWhpxMYDk8NAPiFMGiA062Nt7EGGovsNxuZeFTHPXgwgE4umWJf
MPESA_SHORTCODE=3547179
MPESA_PASSKEY=e0232ed3a06890a62b026b48a7c9ba25e1217825a76312907a1c3cfaffb48856
```

### Fix 3: Callback URL
Update the callback URL in your configuration:
```python
MPESA_CALLBACK_URL=https://your-actual-domain.com/api/mpesa/callback
```

## Testing Commands

### Test 1: Basic Connectivity
```bash
python test_network_connectivity.py
```

### Test 2: STK Push with Better Error Handling
```bash
python test_stk_push_fixed.py
```

### Test 3: Test from Your App
```bash
curl -X GET http://localhost:5000/api/mpesa/test-config
```

## Common Solutions

### Solution 1: Network Issues
- **Problem**: ISP blocking the connection
- **Solution**: Try mobile hotspot or different network

### Solution 2: Firewall Issues
- **Problem**: Firewall blocking outbound HTTPS
- **Solution**: Temporarily disable firewall or add exception

### Solution 3: DNS Issues
- **Problem**: DNS not resolving api.safaricom.co.ke
- **Solution**: Use Google DNS (8.8.8.8, 8.8.4.4)

### Solution 4: Corporate Network
- **Problem**: Corporate proxy/firewall restrictions
- **Solution**: Test from home network or mobile hotspot

## Expected Behavior After Fix

When working correctly, you should see:
```
=== M-Pesa STK Push Test (Fixed) ===

Testing with:
Phone: 254712591937
Amount: 1 KES

0. Testing connectivity...
✅ Basic connectivity: Status 200
✅ Connectivity test passed!

1. Getting access token...
Getting access token from: https://api.safaricom.co.ke
Consumer Key: 3yOAC0yXFi...
Access token response - Status: 200
Response body: {"access_token":"...","expires_in":"3599"}
Access token: [token]...
✅ Access token obtained successfully!

2. Initiating STK Push...
STK Push - Token: [token]..., Password: [password]..., Timestamp: [timestamp]
STK Push payload: {...}
STK Push API Response - Status: 200
Response body: {"CheckoutRequestID":"...","MerchantRequestID":"...","ResponseCode":"0","ResponseDescription":"Success. Request accepted for processing"}
✅ STK Push initiated successfully!
CheckoutRequestID: [ID]
MerchantRequestID: [ID]
ResponseCode: 0
ResponseDescription: Success. Request accepted for processing
```

## Next Steps

1. **Run the diagnostic tests** to identify the specific issue
2. **Try the troubleshooting steps** in order
3. **Test with the improved scripts** that have better error handling
4. **Update your app** with the improved MPESA service code
5. **Test the full payment flow** once connectivity is working

## Support

If the issue persists after trying all steps:
1. Check if you can access other external APIs
2. Try from a different network/location
3. Contact your network administrator if on corporate network
4. Consider using a VPN service 