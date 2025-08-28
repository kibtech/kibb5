#!/usr/bin/env python3
"""
Simple database test script
"""

from app import create_app, db
from app.models import Product, Category, Brand

def test_database():
    """Test database connection and basic operations"""
    print("🧪 Testing database connection...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test basic query
            products = Product.query.all()
            categories = Category.query.all()
            brands = Brand.query.all()
            
            print(f"✅ Database connection successful!")
            print(f"📦 Found {len(products)} products")
            print(f"📂 Found {len(categories)} categories")
            print(f"🏷️  Found {len(brands)} brands")
            
            if products:
                print("📋 Sample products:")
                for product in products[:3]:
                    print(f"  - {product.name} (KSh {product.price})")
            
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False

if __name__ == '__main__':
    test_database() 