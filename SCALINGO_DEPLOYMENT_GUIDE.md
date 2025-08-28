# Scalingo Deployment Guide with CORS Fixes

## 🚀 Overview

This guide ensures your KibTech admin login works properly on Scalingo with all CORS issues resolved.

## ✅ CORS Fixes Applied

1. **Updated CORS Configuration** - Added Scalingo domains to allowed origins
2. **Admin Login Route** - Added CORS headers directly to login endpoint
3. **OPTIONS Route** - Added preflight request handler
4. **Environment Detection** - Automatic CORS configuration based on environment

## 🔧 Environment Variables for Scalingo

Set these environment variables in your Scalingo dashboard:

```bash
# App Configuration
APP_BASE_URL=https://your-app-name.scalingo.io
ENVIRONMENT=production
CUSTOM_DOMAIN=https://kibtech.co.ke

# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security
SECRET_KEY=your-flask-secret-key
JWT_SECRET_KEY=your-super-secret-jwt-key-here

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your-mpesa-consumer-key
MPESA_CONSUMER_SECRET=your-mpesa-consumer-secret
MPESA_SHORTCODE=your-mpesa-shortcode
MPESA_PASSKEY=your-mpesa-passkey

# Email Configuration
BREVO_API_KEY=your-brevo-api-key
```

## 📋 Deployment Steps

### 1. **Prepare Your Code**
```bash
# Ensure all CORS fixes are applied
git add .
git commit -m "Add CORS fixes for Scalingo deployment"
git push origin main
```

### 2. **Deploy to Scalingo**
```bash
# If using Scalingo CLI
scalingo create your-app-name
scalingo git-set-cmd "python run.py"
scalingo deploy
```

### 3. **Set Environment Variables**
- Go to your Scalingo dashboard
- Navigate to Environment tab
- Add all the environment variables listed above

### 4. **Test the Deployment**
```bash
# Test CORS configuration
python fix_production_cors.py
```

## 🔐 Admin Login Credentials

After deployment, you can login with:
- **URL:** `https://your-app-name.scalingo.io/admin`
- **Email:** `kibtechc@gmail.com`
- **Password:** `Kibtechceo@2018`

## 🛠️ Troubleshooting

### If CORS errors persist:

1. **Check Environment Variables**
   ```bash
   # Verify ENVIRONMENT is set to 'production'
   echo $ENVIRONMENT
   ```

2. **Test CORS Headers**
   ```bash
   curl -I -X OPTIONS https://your-app-name.scalingo.io/admin/login
   ```

3. **Check Logs**
   ```bash
   scalingo logs
   ```

### Common Issues:

1. **CORS Still Blocking**
   - Ensure `ENVIRONMENT=production` is set
   - Check that `APP_BASE_URL` matches your Scalingo domain

2. **Admin User Not Found**
   - Run the admin user creation script after deployment
   - Check database connection

3. **Login Fails**
   - Verify JWT_SECRET_KEY is set
   - Check that admin user exists in database

## ✅ Verification Checklist

- [ ] App deployed to Scalingo
- [ ] Environment variables set
- [ ] Database connected
- [ ] Admin user created
- [ ] CORS headers present
- [ ] Admin login works
- [ ] Admin dashboard accessible

## 🎯 Expected Result

After following this guide, you should be able to:
1. Access `https://your-app-name.scalingo.io/admin`
2. Login with the provided credentials
3. Access the full admin dashboard without CORS errors
4. Use all admin functionality

## 📞 Support

If you encounter issues:
1. Check Scalingo logs: `scalingo logs`
2. Test CORS: `python fix_production_cors.py`
3. Verify environment variables are set correctly
4. Ensure database is accessible and admin user exists

---

**Note:** The CORS fixes applied will work for both local development and production deployment on Scalingo. 