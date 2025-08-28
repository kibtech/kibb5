# M-Pesa B2C Withdrawal Setup Guide

## Overview
This guide will help you set up M-Pesa B2C (Business to Customer) withdrawals for your KibTech store.

## Prerequisites
1. **M-Pesa Business Account** with B2C permissions
2. **Daraja API Access** (Consumer Key and Secret)
3. **Business Shortcode** 
4. **Initiator Credentials** for B2C transactions

## Required Credentials

### 1. Basic M-Pesa Credentials
- `MPESA_CONSUMER_KEY` - Your Daraja API consumer key
- `MPESA_CONSUMER_SECRET` - Your Daraja API consumer secret
- `MPESA_SHORTCODE` - Your business shortcode
- `MPESA_PASSKEY` - Your STK Push passkey

### 2. B2C Specific Credentials
- `MPESA_INITIATOR_NAME` - Your business name (e.g., "KibTech Store")
- `MPESA_INITIATOR_PASSWORD` - Your initiator password (encrypted for production)

### 3. Callback URLs
- `MPESA_RESULT_URL` - URL to receive B2C result callbacks
- `MPESA_TIMEOUT_URL` - URL to handle B2C timeout callbacks

## Setup Steps

### Step 1: Configure Environment Variables

Add the following to your `.env` file:

```env
# M-Pesa Configuration
MPESA_CONSUMER_KEY=your_consumer_key_here
MPESA_CONSUMER_SECRET=your_consumer_secret_here
MPESA_SHORTCODE=your_shortcode_here
MPESA_PASSKEY=your_passkey_here

# B2C Configuration
MPESA_INITIATOR_NAME=KibTech Store
MPESA_INITIATOR_PASSWORD=your_initiator_password_here

# Callback URLs
MPESA_RESULT_URL=http://yourdomain.com/api/mpesa/b2c-result
MPESA_TIMEOUT_URL=http://yourdomain.com/api/mpesa/timeout

# Environment
ENVIRONMENT=production
```

### Step 2: Run the Setup Script

```bash
python setup_mpesa_b2c.py
```

This script will:
- Check your current M-Pesa configuration
- Prompt for missing B2C credentials
- Update your `.env` file
- Test the configuration

### Step 3: Test the Configuration

```bash
python test_b2c_withdrawal.py
```

This will test:
- Access token generation
- B2C payment initiation
- Withdrawal logic

## Security Considerations

### Production Environment
For production, you **MUST** encrypt the initiator password using the M-Pesa certificate:

1. **Download the certificate** from your M-Pesa portal
2. **Encrypt the initiator password** using the certificate
3. **Use the encrypted password** as the security credential

### Current Implementation
The current implementation uses plain text passwords for development. For production, you need to:

1. Implement proper certificate-based encryption
2. Store the certificate securely
3. Encrypt passwords before sending to M-Pesa API

## API Endpoints

### Withdrawal Endpoint
```
POST /api/mpesa/withdraw
```

**Request Body:**
```json
{
  "amount": 100,
  "phone_number": "254712345678"
}
```

**Response:**
```json
{
  "message": "Withdrawal initiated successfully",
  "conversation_id": "abc123",
  "withdrawal_id": 1
}
```

### Callback Endpoints
- `POST /api/mpesa/b2c-result` - Receives B2C result
- `POST /api/mpesa/timeout` - Handles timeouts

## Testing

### Test Phone Numbers
For testing, use these M-Pesa test phone numbers:
- `254708374149` - Test customer 1
- `254708374150` - Test customer 2

### Test Amounts
- Minimum: KSh 10
- Maximum: KSh 70,000 (M-Pesa limit)

## Troubleshooting

### Common Issues

1. **"Initiator password not configured"**
   - Add `MPESA_INITIATOR_PASSWORD` to your `.env` file

2. **"Failed to get access token"**
   - Check your `MPESA_CONSUMER_KEY` and `MPESA_CONSUMER_SECRET`
   - Verify your Daraja API access

3. **"B2C payment failed"**
   - Check your `MPESA_INITIATOR_NAME` and `MPESA_INITIATOR_PASSWORD`
   - Verify your shortcode has B2C permissions
   - Check callback URLs are accessible

4. **"Insufficient balance"**
   - User doesn't have enough balance for withdrawal
   - Check both commission and deposited balances

### Debug Mode
Enable debug logging by setting:
```env
FLASK_ENV=development
FLASK_DEBUG=1
```

## Production Checklist

- [ ] Configure encrypted initiator password
- [ ] Set up proper callback URLs
- [ ] Test with real phone numbers
- [ ] Monitor transaction logs
- [ ] Set up error notifications
- [ ] Implement retry logic for failed transactions

## Support

For M-Pesa API issues:
- Check the [Daraja API Documentation](https://developer.safaricom.co.ke/)
- Contact Safaricom Developer Support
- Review your M-Pesa portal for transaction status

For application issues:
- Check the application logs
- Run the test scripts
- Verify all environment variables are set correctly 