# KibTech OTP & Email System

A comprehensive email verification and transactional messaging system for KibTech Online Services.

## 🚀 Features

### ✉️ Email OTP Verification for Signup
- 6-digit numeric OTP generation
- 10-minute expiry with automatic cleanup
- Rate limiting (2-minute cooldown)
- Brevo SMTP integration
- Professional HTML email templates

### 🔁 OTP Verification for Password Reset
- Secure password reset via email OTP
- Same security features as signup verification
- One-time use OTPs with automatic invalidation

### 📦 Order Confirmation Emails
- Automatic order confirmation emails
- Detailed order information
- Professional email templates
- Non-blocking email sending

## 🏗️ Architecture

### Database Models

#### User Model Updates
```python
email_verified = db.Column(db.Boolean, default=False)  # New field
otps = db.relationship('OTP', backref='user', lazy='dynamic')  # New relationship
```

#### OTP Model
```python
class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)  # 6-digit OTP
    purpose = db.Column(db.String(50), nullable=False)  # 'email_verification', 'password_reset'
    is_used = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Service Layer

#### EmailService (`app/services/email_service.py`)
- Brevo SMTP integration
- HTML email templates
- Error handling and logging

#### OTPService (`app/services/otp_service.py`)
- OTP generation with secure random numbers
- Rate limiting to prevent abuse
- Automatic cleanup of expired OTPs
- Validation and verification logic

### API Endpoints

#### Authentication Routes (`/api/auth/`)
- `POST /register` - User registration with email verification
- `POST /login` - Login (requires email verification)
- `POST /verify-email` - Verify email with OTP
- `POST /resend-verification` - Resend verification OTP
- `POST /forgot-password` - Send password reset OTP
- `POST /reset-password` - Reset password with OTP

## 🔧 Configuration

### Environment Variables
```bash
# Email Configuration (Brevo SMTP)
MAIL_SERVER=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=93a1ce001@smtp-brevo.com
MAIL_PASSWORD=pw2VX3bZBEScz4T7
MAIL_DEFAULT_SENDER=kibtechc@gmail.com
MAIL_DEFAULT_SENDER_NAME=KibTech Online Services

# OTP Configuration
OTP_EXPIRY_MINUTES=10
OTP_LENGTH=6
OTP_RATE_LIMIT_MINUTES=2
```

### Database Migration
Run the migration script to add OTP functionality:
```bash
python migrate_otp.py
```

## 📡 API Usage Examples

### User Registration with Email Verification
```javascript
// 1. Register user
const response = await fetch('/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    phone: '+254700000000',
    password: 'securepassword123'
  })
});

// 2. User receives email with OTP
// 3. User verifies email
const verifyResponse = await fetch('/api/auth/verify-email', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com',
    otp: '123456'
  })
});

// 4. User can now login
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'securepassword123'
  })
});
```

### Password Reset Flow
```javascript
// 1. Request password reset
const resetRequest = await fetch('/api/auth/forgot-password', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com'
  })
});

// 2. User receives email with OTP
// 3. Reset password with OTP
const resetPassword = await fetch('/api/auth/reset-password', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'john@example.com',
    otp: '123456',
    new_password: 'newsecurepassword123'
  })
});
```

## 🔐 Security Features

### OTP Security
- Cryptographically secure random number generation
- One-time use OTPs with automatic invalidation
- Rate limiting to prevent brute force attacks
- Automatic expiry with cleanup

### Email Security
- TLS encryption for all email communications
- Secure SMTP authentication with Brevo
- Input validation and sanitization
- Error handling without information leakage

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migration
```bash
python migrate_otp.py
```

### 3. Configure Environment Variables
Create a `.env` file with your Brevo SMTP credentials.

### 4. Test Email Functionality
```bash
python -c "
from app import create_app
from app.services.email_service import email_service

app = create_app()
with app.app_context():
    success, message = email_service.send_email(
        'test@example.com',
        'Test Email',
        '<h1>Test Email</h1><p>This is a test email.</p>'
    )
    print(f'Email sent: {success}, Message: {message}')
"
```

## 🚨 Troubleshooting

### Email Not Sending
1. Check SMTP credentials in config
2. Verify Brevo account is active
3. Check firewall settings
4. Review email logs for error messages

### OTP Not Working
1. Check database migration was successful
2. Verify OTP table exists in database
3. Check rate limiting settings
4. Review application logs for errors

---

**KibTech OTP & Email System** - Secure, reliable email verification and transactional messaging 