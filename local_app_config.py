#!/usr/bin/env python3
"""
Local App Configuration for KibTech Store
This ensures the app can run locally with proper configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_local_config():
    """Get local configuration for development"""
    return {
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'your-flask-secret-key-local-dev'),
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL', 'sqlite:///kibtech_local.db'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', 'your-super-secret-jwt-key-here-local-dev'),
        'JWT_ACCESS_TOKEN_EXPIRES': False,
        'DEBUG': True,
        'ENVIRONMENT': 'development',
        # M-Pesa Configuration for local development
        'MPESA_CONSUMER_KEY': os.environ.get('MPESA_CONSUMER_KEY'),
        'MPESA_CONSUMER_SECRET': os.environ.get('MPESA_CONSUMER_SECRET'),
        'MPESA_SHORTCODE': os.environ.get('MPESA_SHORTCODE'),
        'MPESA_PASSKEY': os.environ.get('MPESA_PASSKEY'),
        'MPESA_INITIATOR_NAME': os.environ.get('MPESA_INITIATOR_NAME'),
        'MPESA_INITIATOR_PASSWORD': os.environ.get('MPESA_INITIATOR_PASSWORD'),
        'MPESA_CALLBACK_URL': os.environ.get('MPESA_CALLBACK_URL', 'http://localhost:5000/api/mpesa/callback'),
        'MPESA_RESULT_URL': os.environ.get('MPESA_RESULT_URL', 'https://kibtech.co.ke/api/mpesa/b2c-result'),
        'MPESA_TIMEOUT_URL': os.environ.get('MPESA_TIMEOUT_URL', 'https://kibtech.co.ke/api/mpesa/timeout'),
        'MPESA_BASE_URL': os.environ.get('MPESA_BASE_URL', 'https://api.safaricom.co.ke'),
        # Email Configuration
        'BREVO_API_KEY': os.environ.get('BREVO_API_KEY'),
        'BREVO_SMTP_SERVER': os.environ.get('BREVO_SMTP_SERVER'),
        'BREVO_SMTP_PORT': int(os.environ.get('BREVO_SMTP_PORT', 587)),
        'BREVO_SMTP_LOGIN': os.environ.get('BREVO_SMTP_LOGIN'),
        'BREVO_SMTP_PASSWORD': os.environ.get('BREVO_SMTP_PASSWORD'),
        'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER'),
        'MAIL_DEFAULT_SENDER_NAME': os.environ.get('MAIL_DEFAULT_SENDER_NAME'),
        'MAIL_DEFAULT_REPLY_TO': os.environ.get('MAIL_DEFAULT_REPLY_TO'),
    }

if __name__ == "__main__":
    config = get_local_config()
    print("Local configuration loaded successfully!")
    print(f"Database URI: {config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Environment: {config['ENVIRONMENT']}")
    print(f"Debug Mode: {config['DEBUG']}")
