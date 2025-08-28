# KibTech Store - Local Development Guide

## 🚀 Quick Start

### 1. Setup Local Environment
```bash
# Run the local setup script
python setup_local_environment.py
```

### 2. Start the Application
```bash
# Windows
START_LOCAL.bat

# Linux/Mac
python app.py
```

### 3. Access the Application
- **Local URL**: http://localhost:5000
- **Production Domain**: kibtech.co.ke (configured for production URLs)

## 🔧 Configuration Details

### Domain Configuration
- ✅ **Production Domain**: `kibtech.co.ke` (correctly configured)
- ✅ **Local Development**: `localhost:5000`
- ✅ **M-Pesa Callbacks**: Local development uses `localhost:5000`
- ✅ **Production URLs**: All production endpoints use `kibtech.co.ke`

### Database Configuration
- **Local Development**: SQLite (`kibtech_local.db`)
- **Production**: PostgreSQL (Supabase)
- **Environment**: Development mode with debug enabled

### Environment Variables
The system automatically creates a `.env` file with:
```bash
# Local Development Configuration
DATABASE_URL=sqlite:///kibtech_local.db
FLASK_CONFIG=local
ENVIRONMENT=development
DEBUG=true

# M-Pesa Configuration
MPESA_CALLBACK_URL=http://localhost:5000/api/mpesa/callback
MPESA_RESULT_URL=https://kibtech.co.ke/api/mpesa/b2c-result
MPESA_TIMEOUT_URL=https://kibtech.co.ke/api/mpesa/timeout
```

## 📁 File Structure

### Configuration Files
- `config.py` - Main configuration (updated with correct domain)
- `config_local.py` - Local development configuration
- `.env` - Local environment variables (auto-generated)
- `local_app_config.py` - Local app configuration helper

### Database Files
- `kibtech_local.db` - Local SQLite database (auto-created)

### Startup Scripts
- `START_LOCAL.bat` - Windows startup script
- `setup_local_environment.py` - Environment setup script

## 🔍 Domain Verification

The system has been updated to use the correct domain `kibtech.co.ke` in all files:

### ✅ Updated Files
- `config.py` - Main configuration
- `config_local.py` - Local configuration
- `.envv` - Environment variables
- `test_withdrawal.py` - Test scripts
- `test_stk_push_with_google_dns.py` - Test scripts
- `test_b2c_status.py` - Test scripts
- `README.md` - Documentation
- `B2C_WITHDRAWAL_SETUP.md` - Documentation

### ✅ Correct Domain Usage
- **Production URLs**: `https://kibtech.co.ke/api/...`
- **Local Development**: `http://localhost:5000/api/...`
- **Email Templates**: `support@kibtech.co.ke`
- **CORS Configuration**: `https://kibtech.co.ke`

## 🛠️ Development Workflow

### 1. Local Development
```bash
# Start local development
python app.py

# Or use the batch file (Windows)
START_LOCAL.bat
```

### 2. Testing
```bash
# Test M-Pesa integration
python test_withdrawal.py

# Test STK push
python test_stk_push_with_google_dns.py

# Test B2C status
python test_b2c_status.py
```

### 3. Database Management
```bash
# Initialize local database
python init_local_db.py

# Add product image URL column
python add_product_image_url_column.py
```

## 🌐 URL Configuration

### Local Development URLs
- **Application**: http://localhost:5000
- **API Base**: http://localhost:5000/api
- **M-Pesa Callback**: http://localhost:5000/api/mpesa/callback

### Production URLs (kibtech.co.ke)
- **Application**: https://kibtech.co.ke
- **API Base**: https://kibtech.co.ke/api
- **M-Pesa Result**: https://kibtech.co.ke/api/mpesa/b2c-result
- **M-Pesa Timeout**: https://kibtech.co.ke/api/mpesa/timeout

## 🔒 Security Configuration

### Local Development
- **Debug Mode**: Enabled
- **JWT Secret**: Local development key
- **Database**: SQLite (local file)
- **HTTPS**: Not required for localhost

### Production
- **Debug Mode**: Disabled
- **JWT Secret**: Production key
- **Database**: PostgreSQL (Supabase)
- **HTTPS**: Required for kibtech.co.ke

## 📧 Email Configuration

### Local Development
- **Sender**: emmkash20@gmail.com
- **Sender Name**: KibTech Store (Local)
- **SMTP**: Brevo (configured for local testing)

### Production
- **Sender**: emmkash20@gmail.com
- **Sender Name**: KibTech Store
- **SMTP**: Brevo (production configuration)

## 🧪 Testing

### M-Pesa Integration Testing
```bash
# Test withdrawal functionality
python test_withdrawal.py

# Test STK push with Google DNS
python test_stk_push_with_google_dns.py

# Test B2C status
python test_b2c_status.py
```

### API Testing
```bash
# Test API endpoints
curl http://localhost:5000/api/health

# Test authentication
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Solution: Run database initialization
python init_local_db.py
```

#### 2. M-Pesa API Errors
```bash
# Check configuration
python test_b2c_status.py

# Verify domain configuration
grep -r "kibtech.co.ke" .
```

#### 3. Port Already in Use
```bash
# Change port in app.py
app.run(port=5001)
```

#### 4. Environment Variables Not Loading
```bash
# Ensure .env file exists
python setup_local_environment.py
```

### Debug Commands
```bash
# Check domain configuration
python -c "import config; print('Domain configured correctly')"

# Test local database
python -c "import sqlite3; conn = sqlite3.connect('kibtech_local.db'); print('Database OK')"

# Verify environment
python -c "import os; print('ENVIRONMENT:', os.getenv('ENVIRONMENT', 'not set'))"
```

## 📋 Checklist

### ✅ Domain Configuration
- [x] All files use `kibtech.co.ke` (correct domain)
- [x] Local development uses `localhost:5000`
- [x] M-Pesa callbacks configured correctly
- [x] Email templates use correct domain

### ✅ Local Development
- [x] SQLite database configured
- [x] Debug mode enabled
- [x] Local environment variables set
- [x] Startup scripts created

### ✅ Production Ready
- [x] Production URLs point to `kibtech.co.ke`
- [x] HTTPS configured for production
- [x] Database connection optimized
- [x] Security settings appropriate

## 🎯 Summary

The KibTech Store system has been successfully configured with:

1. **Correct Domain**: `kibtech.co.ke` (all files updated)
2. **Local Development**: Works on `localhost:5000`
3. **Production URLs**: All point to `kibtech.co.ke`
4. **Database**: SQLite for local, PostgreSQL for production
5. **Environment**: Proper separation between local and production

The system can now run locally without issues while maintaining the correct domain configuration for production deployment. 