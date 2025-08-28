# Heroku Database Setup Guide

## 🚀 Overview

This guide explains how to set up the KibTech Store database on Heroku with automatic seeding of default products and services.

## 📋 Prerequisites

1. **Heroku Account** - Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI** - Install from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git Repository** - Your KibTech Store code pushed to GitHub

## 🗄️ Database Setup

### Step 1: Add PostgreSQL to Heroku

```bash
# Add PostgreSQL addon to your Heroku app
heroku addons:create heroku-postgresql:mini

# Verify the database URL
heroku config:get DATABASE_URL
```

### Step 2: Set Environment Variables

```bash
# Set the configuration for Heroku
heroku config:set FLASK_CONFIG=heroku

# Set M-Pesa configuration
heroku config:set MPESA_CONSUMER_KEY=your_consumer_key
heroku config:set MPESA_CONSUMER_SECRET=your_consumer_secret
heroku config:set MPESA_SHORTCODE=3547179
heroku config:set MPESA_PASSKEY=your_passkey
heroku config:set MPESA_CALLBACK_URL=https://kibtech.co.ke/api/mpesa/callback
heroku config:set MPESA_RESULT_URL=https://kibtech.co.ke/api/mpesa/b2c-result
heroku config:set MPESA_TIMEOUT_URL=https://kibtech.co.ke/api/mpesa/timeout

# Set other required variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret-key
heroku config:set ENVIRONMENT=production
```

### Step 3: Deploy Your Application

```bash
# Deploy to Heroku
git push heroku main

# Or if using master branch
git push heroku master
```

## 🌱 Database Seeding on Heroku

### Option 1: Automatic Seeding (Recommended)

The application automatically seeds the database on startup. Just deploy and it will work:

```bash
# Deploy and the database will be seeded automatically
git push heroku main
```

### Option 2: Manual Seeding

If you need to manually seed the database:

```bash
# Run the database setup script on Heroku
heroku run python setup_heroku_database.py --heroku
```

### Option 3: Using Heroku Console

```bash
# Open Heroku console
heroku run python

# In the Python console:
>>> from app import create_app, db
>>> from app.models import User, Product, Category
>>> app = create_app('heroku')
>>> with app.app_context():
...     db.create_all()
...     # Add your seeding code here
```

## 🔧 Database Migration

### Run Migrations

```bash
# Run database migrations on Heroku
heroku run flask db upgrade
```

### Reset Database (if needed)

```bash
# Reset the database (WARNING: This will delete all data)
heroku pg:reset DATABASE_URL --confirm your-app-name

# Then seed the database
heroku run python setup_heroku_database.py --heroku
```

## 📊 Verify Database Setup

### Check Database Status

```bash
# Check if tables exist
heroku run python -c "
from app import create_app, db
from app.models import Product, Category, User
app = create_app('heroku')
with app.app_context():
    print(f'Products: {Product.query.count()}')
    print(f'Categories: {Category.query.count()}')
    print(f'Admin Users: {User.query.filter_by(is_admin=True).count()}')
"
```

### Check Database Connection

```bash
# Test database connection
heroku run python -c "
from app import create_app
app = create_app('heroku')
print('Database connection OK')
"
```

## 🎯 What Gets Added Automatically

### Categories (4)
- Laptops
- Smartphones  
- Accessories
- Cyber Services

### Products (9)
- MacBook Pro 14" M2 - KSh 249,999
- Dell XPS 13 Plus - KSh 189,999
- iPhone 15 Pro - KSh 189,999
- Samsung Galaxy S24 Ultra - KSh 179,999
- AirPods Pro 2nd Gen - KSh 29,999
- Samsung Galaxy Watch 6 - KSh 39,999
- Website Security Audit - KSh 49,999
- Network Security Setup - KSh 79,999
- Data Recovery Service - KSh 29,999

### Admin User
- Email: admin@kibtech.co.ke
- Password: admin123 (change in production)

## 🔍 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```bash
# Check if PostgreSQL is attached
heroku addons

# Check database URL
heroku config:get DATABASE_URL
```

#### 2. Migration Errors
```bash
# Reset migrations
heroku run flask db stamp head
heroku run flask db migrate
heroku run flask db upgrade
```

#### 3. Seeding Errors
```bash
# Check if tables exist
heroku run python -c "
from app import create_app, db
app = create_app('heroku')
with app.app_context():
    db.create_all()
    print('Tables created')
"
```

#### 4. Application Errors
```bash
# Check application logs
heroku logs --tail

# Check specific errors
heroku logs --source app
```

### Debug Commands

```bash
# Check Heroku app status
heroku ps

# Check environment variables
heroku config

# Check database status
heroku pg:info

# Connect to database directly
heroku pg:psql
```

## 🚀 Deployment Checklist

### Before Deployment
- [ ] PostgreSQL addon added to Heroku
- [ ] Environment variables set
- [ ] Code pushed to GitHub
- [ ] Domain configured (kibtech.co.ke)

### After Deployment
- [ ] Application starts without errors
- [ ] Database tables created
- [ ] Default products seeded
- [ ] Admin user created
- [ ] API endpoints working
- [ ] Frontend accessible

### Production Verification
- [ ] Store loads with products
- [ ] Admin panel accessible
- [ ] M-Pesa integration working
- [ ] Domain redirects correctly
- [ ] SSL certificate active

## 📈 Monitoring

### Check Application Status
```bash
# View application logs
heroku logs --tail

# Check database performance
heroku pg:ps
```

### Monitor Database
```bash
# Check database size
heroku pg:info

# View slow queries
heroku pg:outliers
```

## 🔒 Security

### Change Default Passwords
```bash
# Update admin password in production
heroku run python -c "
from app import create_app, db
from app.models import User
app = create_app('heroku')
with app.app_context():
    admin = User.query.filter_by(email='admin@kibtech.co.ke').first()
    if admin:
        admin.set_password('new-secure-password')
        db.session.commit()
        print('Admin password updated')
"
```

### Environment Variables
Make sure all sensitive data is in environment variables:
- Database credentials
- API keys
- Secret keys
- Passwords

## 🎉 Success!

Once everything is set up, your KibTech Store will be available at:
- **Production URL**: https://kibtech.co.ke
- **Admin Panel**: https://kibtech.co.ke/admin
- **API Base**: https://kibtech.co.ke/api

The database will automatically contain all default products and services, ready for customers to browse and purchase. 