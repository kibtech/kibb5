#!/bin/bash

echo "========================================"
echo "KibTech Store - Complete Setup"
echo "========================================"
echo

echo "🚀 Setting up KibTech Store with default products and services..."
echo

echo "📋 Step 1: Setting up local environment..."
python3 setup_local_environment.py
if [ $? -ne 0 ]; then
    echo "❌ Environment setup failed!"
    exit 1
fi

echo
echo "📦 Step 2: Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Dependency installation failed!"
    exit 1
fi

echo
echo "🗄️ Step 3: Initializing database..."
python3 init_local_db.py
if [ $? -ne 0 ]; then
    echo "❌ Database initialization failed!"
    exit 1
fi

echo
echo "🌱 Step 4: Seeding database with default products and services..."
python3 auto_seed_database.py
if [ $? -ne 0 ]; then
    echo "❌ Database seeding failed!"
    exit 1
fi

echo
echo "🔧 Step 5: Adding product image URL column..."
python3 add_product_image_url_column.py
if [ $? -ne 0 ]; then
    echo "❌ Database migration failed!"
    exit 1
fi

echo
echo "========================================"
echo "✅ Setup completed successfully!"
echo "========================================"
echo
echo "📊 What was added:"
echo "- 4 Product Categories (Laptops, Smartphones, Accessories, Cyber Services)"
echo "- 9 Tech Products (Laptops, Smartphones, Accessories)"
echo "- 6 Cyber Services (Security, Recovery, Training, etc.)"
echo "- 1 Admin User (admin@kibtech.co.ke / admin123)"
echo
echo "🌐 Access your store:"
echo "- Local: http://localhost:5000"
echo "- Production: https://kibtech.co.ke"
echo
echo "🔑 Admin Login:"
echo "- Email: admin@kibtech.co.ke"
echo "- Password: admin123 (change in production)"
echo
echo "🚀 Starting the application..."
echo
python3 wsgi.py 