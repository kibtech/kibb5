# KIBTECH Heroku Deployment Guide

This guide will help you deploy the KIBTECH Online Services application to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your project is in a Git repository

## Quick Deployment

### Option 1: Automated Deployment Script

1. Run the automated deployment script:
```bash
   python deploy_to_heroku.py
   ```

2. Follow the prompts to:
   - Create a new Heroku app (or use existing)
   - Set up PostgreSQL database
   - Configure environment variables
   - Deploy the application

### Option 2: Manual Deployment

#### Step 1: Login to Heroku
```bash
heroku login
```

#### Step 2: Create Heroku App
```bash
heroku create your-app-name
```

#### Step 3: Configure Supabase Database
```bash
heroku config:set DATABASE_URL=postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres
```

#### Step 4: Set Environment Variables
```bash
# Essential variables
heroku config:set FLASK_CONFIG=heroku
heroku config:set ENVIRONMENT=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(24))")
heroku config:set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# M-Pesa Configuration (update with your values)
heroku config:set MPESA_CONSUMER_KEY=your_consumer_key
heroku config:set MPESA_CONSUMER_SECRET=your_consumer_secret
heroku config:set MPESA_SHORTCODE=your_shortcode
heroku config:set MPESA_PASSKEY=your_passkey
heroku config:set MPESA_INITIATOR_NAME=your_initiator_name
heroku config:set MPESA_INITIATOR_PASSWORD=your_initiator_password
heroku config:set MPESA_SECURITY_CREDENTIAL=your_security_credential

# Email Configuration (update with your values)
heroku config:set BREVO_API_KEY=your_brevo_api_key
heroku config:set BREVO_SMTP_SERVER=smtp-relay.brevo.com
heroku config:set BREVO_SMTP_PORT=587
heroku config:set BREVO_SMTP_LOGIN=your_smtp_login
heroku config:set BREVO_SMTP_PASSWORD=your_smtp_password
heroku config:set MAIL_DEFAULT_SENDER=your_email@kibtech.coke
heroku config:set MAIL_DEFAULT_SENDER_NAME=KibTech Store
heroku config:set MAIL_DEFAULT_REPLY_TO=your_email@kibtech.coke
```

#### Step 5: Deploy Application
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Step 6: Run Database Migrations
```bash
heroku run python -m flask db upgrade
```

#### Step 7: Open the App
```bash
heroku open
```

## Configuration Files

### Procfile
```
web: gunicorn app:app
```

### runtime.txt
```
python-3.11.7
```

### requirements.txt
The requirements file includes all necessary dependencies for Heroku deployment.

## Environment Variables

### Required Variables
- `FLASK_CONFIG`: Set to 'heroku' for production
- `ENVIRONMENT`: Set to 'production'
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT signing key
- `DATABASE_URL`: Automatically set by Heroku PostgreSQL addon

### M-Pesa Configuration
- `MPESA_CONSUMER_KEY`: Your M-Pesa consumer key
- `MPESA_CONSUMER_SECRET`: Your M-Pesa consumer secret
- `MPESA_SHORTCODE`: Your M-Pesa shortcode
- `MPESA_PASSKEY`: Your M-Pesa passkey
- `MPESA_INITIATOR_NAME`: Your initiator name
- `MPESA_INITIATOR_PASSWORD`: Your initiator password
- `MPESA_SECURITY_CREDENTIAL`: Your security credential

### Email Configuration
- `BREVO_API_KEY`: Your Brevo API key
- `BREVO_SMTP_SERVER`: SMTP server (smtp-relay.brevo.com)
- `BREVO_SMTP_PORT`: SMTP port (587)
- `BREVO_SMTP_LOGIN`: Your SMTP login
- `BREVO_SMTP_PASSWORD`: Your SMTP password
- `MAIL_DEFAULT_SENDER`: Default sender email
- `MAIL_DEFAULT_SENDER_NAME`: Default sender name
- `MAIL_DEFAULT_REPLY_TO`: Reply-to email address

## Frontend Configuration

After deploying the backend, update your frontend configuration:

1. **Update API Base URL**: Change your frontend API calls to use the Heroku URL
   ```javascript
   // Example: Update your API base URL
   const API_BASE_URL = 'https://kibtech.coke/api';
   ```

2. **Update CORS Origins**: Update the CORS configuration in `app/__init__.py` with your frontend domain

3. **Deploy Frontend**: Deploy your React frontend to:
   - Netlify
   - Vercel
   - Heroku (separate app)
   - Or any other hosting service

## Database Management

### View Database
```bash
heroku pg:psql
```

### Reset Database
```bash
heroku pg:reset DATABASE_URL
heroku run python -m flask db upgrade
```

### Backup Database
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

## Monitoring and Logs

### View Logs
```bash
heroku logs --tail
```

### Monitor Performance
```bash
heroku ps
```

### Check Database Status
```bash
heroku pg:info
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure `Procfile` is correctly formatted
   - Verify Python version in `runtime.txt`

2. **Database Connection Issues**
   - Ensure PostgreSQL addon is active
   - Check `DATABASE_URL` environment variable
   - Run migrations: `heroku run python -m flask db upgrade`

3. **Static Files Not Loading**
   - WhiteNoise is configured for static file serving
   - Ensure static files are in the `static/` directory

4. **CORS Issues**
   - Update CORS origins in `app/__init__.py`
   - Ensure frontend domain is included in allowed origins

### Debug Commands

```bash
# Check app status
heroku ps

# View recent logs
heroku logs --tail

# Run commands on Heroku
heroku run python -c "from app import create_app; app = create_app('heroku'); print('App created successfully')"

# Check environment variables
heroku config

# Restart the app
heroku restart
```

## Scaling

### Upgrade Database Plan
```bash
heroku addons:upgrade heroku-postgresql:mini
```

### Scale Web Dynos
```bash
heroku ps:scale web=2
```

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to Git
2. **Database Security**: Use strong passwords and enable SSL
3. **API Keys**: Rotate API keys regularly
4. **HTTPS**: Heroku provides SSL certificates automatically

## Cost Optimization

- **Database**: Start with `heroku-postgresql:mini` ($5/month)
- **Dynos**: Use `eco` dynos for development ($5/month)
- **Addons**: Only add necessary addons

## Support

For issues with:
- **Heroku Platform**: [devcenter.heroku.com/support](https://devcenter.heroku.com/support)
- **Application**: Check logs with `heroku logs --tail`
- **Database**: Use `heroku pg:psql` to connect directly

## Next Steps

After successful deployment:

1. **Test All Features**: Ensure all functionality works in production
2. **Set Up Monitoring**: Configure logging and monitoring
3. **Configure Domain**: Set up custom domain if needed
4. **Set Up CI/CD**: Configure automatic deployments
5. **Backup Strategy**: Set up regular database backups
6. **Performance Optimization**: Monitor and optimize as needed 