# KIBTECH ONLINE SERVICES - Premium Tech E-commerce Platform

A complete tech e-commerce store with referral rewards system and M-Pesa integration, built with Flask (Python) backend and React frontend.

## 🚀 Features

### Core Features
- **User Authentication**: JWT-based authentication with referral code system
- **Product Management**: Browse and purchase products
- **M-Pesa Integration**: STK Push for payments and B2C for withdrawals
- **Referral System**: Earn 20% commission on referred user purchases
- **Wallet Management**: Track earnings and withdraw to M-Pesa
- **Order Tracking**: Complete order management system

### Technical Features
- **Backend**: Flask + PostgreSQL + SQLAlchemy
- **Frontend**: React + Tailwind CSS + Axios
- **Payment Gateway**: Safaricom M-Pesa Daraja API
- **Authentication**: JWT tokens
- **Database**: PostgreSQL with Alembic migrations

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- M-Pesa Daraja API credentials (sandbox or production)

## 🛠️ Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kibtech-store
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/kibtech_store_db
   JWT_SECRET_KEY=your-super-secret-jwt-key
   SECRET_KEY=your-flask-secret-key
   
   # M-Pesa Daraja API
   MPESA_CONSUMER_KEY=your_consumer_key
   MPESA_CONSUMER_SECRET=your_consumer_secret
   MPESA_SHORTCODE=174379
   MPESA_PASSKEY=your_passkey
   MPESA_INITIATOR_NAME=testapi
   MPESA_INITIATOR_PASSWORD=your_initiator_password
   MPESA_CALLBACK_URL=https://kibtech.co.ke/api/mpesa/callback
MPESA_RESULT_URL=https://kibtech.co.ke/api/mpesa/b2c-result
MPESA_TIMEOUT_URL=https://kibtech.co.ke/api/mpesa/timeout
   ENVIRONMENT=sandbox
   ```

5. **Set up database**
   ```bash
   # Create database
   createdb kibtech_store_db
   
   # Initialize migrations
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the backend**
   ```bash
   python run.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

The application will be available at:
- Backend: http://localhost:5000
- Frontend: https://kibtech.coke

## 🏗️ Project Structure

```
kibtech-store/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── products/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── orders/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── mpesa/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── services.py
│   └── wallet/
│       ├── __init__.py
│       └── routes.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── pages/
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── migrations/
├── config.py
├── run.py
└── requirements.txt
```

## 📊 Database Schema

### Tables
- **users**: User accounts with referral codes
- **products**: Product catalog
- **orders**: Purchase orders
- **payments**: M-Pesa payment records
- **commissions**: Referral commissions
- **wallets**: User wallet balances
- **withdrawals**: Withdrawal requests

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/referral-stats` - Get referral statistics

### Products
- `GET /api/products/` - List all products
- `GET /api/products/<id>` - Get single product
- `POST /api/products/` - Create product (admin)
- `PUT /api/products/<id>` - Update product (admin)

### Orders
- `POST /api/orders/` - Create order
- `GET /api/orders/` - Get user orders
- `GET /api/orders/<id>` - Get single order
- `PUT /api/orders/<id>/cancel` - Cancel order

### M-Pesa
- `POST /api/mpesa/stk-push` - Initiate STK Push
- `POST /api/mpesa/callback` - STK Push callback
- `POST /api/mpesa/withdraw` - Initiate withdrawal
- `POST /api/mpesa/b2c-result` - B2C result callback

### Wallet
- `GET /api/wallet/balance` - Get wallet balance
- `GET /api/wallet/stats` - Get wallet statistics
- `GET /api/wallet/commissions` - Get commission history
- `GET /api/wallet/withdrawals` - Get withdrawal history
- `GET /api/wallet/referrals` - Get referral details

## 💰 M-Pesa Integration

### STK Push (Customer to Business)
1. User clicks "Buy Now" on a product
2. System creates an order
3. STK Push is initiated to user's phone
4. User enters M-Pesa PIN
5. Payment confirmation updates order status
6. Commission is calculated for referrer (if applicable)

### B2C (Business to Customer)
1. User requests withdrawal (minimum KSh 100)
2. System initiates B2C payment
3. Money is sent to user's M-Pesa number
4. Wallet balance is updated

## 🎯 Referral System

1. **Registration**: Users get unique referral codes
2. **Sharing**: Users share referral links (`/register?ref=CODE`)
3. **Commission**: 20% commission on referred user purchases
4. **Tracking**: Complete referral analytics and earnings

## 🚀 Deployment

### Backend Deployment (Heroku/Railway)
1. Set up production database
2. Configure environment variables
3. Run database migrations
4. Deploy application

### Frontend Deployment (Netlify/Vercel)
1. Build the React app: `npm run build`
2. Deploy the build folder
3. Configure API proxy settings

## 🔒 Security Features

- JWT token authentication
- Password hashing with bcrypt
- Input validation and sanitization
- CORS configuration
- SQL injection prevention with SQLAlchemy ORM

## 🧪 Testing

### Backend Tests
```bash
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📱 Mobile Responsiveness

The frontend is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Progressive Web App (PWA) ready

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@kibtech.coke or create an issue in the repository.

## 🎉 Features Coming Soon

- [ ] Admin dashboard
- [ ] Product categories
- [ ] Order fulfillment tracking
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Multi-level referrals
- [ ] Promotional codes
- [ ] Analytics dashboard