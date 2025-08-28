# Heroku Deployment Checklist

## Pre-Deployment
- [ ] Install Heroku CLI
- [ ] Login to Heroku (`heroku login`)
- [ ] Ensure project is in Git repository
- [ ] Test application locally

## Deployment Steps
- [ ] Create Heroku app (`heroku create your-app-name`)
- [ ] Configure Supabase database (`heroku config:set DATABASE_URL=postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres`)
- [ ] Set environment variables (see HEROKU_DEPLOYMENT.md)
- [ ] Deploy application (`git push heroku main`)
- [ ] Run database migrations (`heroku run python -m flask db upgrade`)
- [ ] Test the deployed application

## Post-Deployment
- [ ] Update frontend API URL to Heroku domain
- [ ] Test all features in production
- [ ] Configure custom domain (if needed)
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

## Environment Variables to Set
- [ ] `FLASK_CONFIG=heroku`
- [ ] `ENVIRONMENT=production`
- [ ] `SECRET_KEY` (auto-generated)
- [ ] `JWT_SECRET_KEY` (auto-generated)
- [ ] `MPESA_CONSUMER_KEY`
- [ ] `MPESA_CONSUMER_SECRET`
- [ ] `MPESA_SHORTCODE`
- [ ] `MPESA_PASSKEY`
- [ ] `MPESA_INITIATOR_NAME`
- [ ] `MPESA_INITIATOR_PASSWORD`
- [ ] `MPESA_SECURITY_CREDENTIAL`
- [ ] `BREVO_API_KEY`
- [ ] `BREVO_SMTP_LOGIN`
- [ ] `BREVO_SMTP_PASSWORD`
- [ ] `MAIL_DEFAULT_SENDER`

## Quick Commands
```bash
# Deploy
python deploy_to_heroku.py

# Or manually:
heroku create your-app-name
heroku config:set DATABASE_URL=postgresql://postgres.fcrvabkgdhdvprwwlyuf:Kibtech@aws-0-eu-west-2.pooler.supabase.com:6543/postgres
heroku config:set FLASK_CONFIG=heroku
heroku config:set ENVIRONMENT=production
git push heroku main
heroku run python -m flask db upgrade
heroku open
```

## Troubleshooting
- [ ] Check logs: `heroku logs --tail`
- [ ] Restart app: `heroku restart`
- [ ] Check database: `heroku pg:psql`
- [ ] View config: `heroku config` 