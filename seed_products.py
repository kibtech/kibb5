#!/usr/bin/env python3
"""
Seed script to add sample products, categories, and brands to the database
Run with: python seed_products.py
"""

from app import create_app, db
from app.models import Product, Category, Brand, ProductImage
from decimal import Decimal
import random

def seed_data():
    app = create_app()
    
    with app.app_context():
        # Check if data already exists
        if Product.query.first():
            print("Data already exists in database. Skipping seed.")
            return
        
        print("Creating categories...")
        # Create categories
        categories_data = [
            {'name': 'Smartphones', 'slug': 'smartphones', 'description': 'Latest smartphones and mobile devices'},
            {'name': 'Laptops', 'slug': 'laptops', 'description': 'High-performance laptops and notebooks'},
            {'name': 'Audio', 'slug': 'audio', 'description': 'Headphones, speakers, and audio equipment'},
            {'name': 'Tablets', 'slug': 'tablets', 'description': 'Tablets and iPad devices'},
            {'name': 'Accessories', 'slug': 'accessories', 'description': 'Tech accessories and gadgets'},
            {'name': 'Cameras', 'slug': 'cameras', 'description': 'Digital cameras and photography equipment'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data, is_active=True)
            db.session.add(category)
            categories.append(category)
        
        print("Creating brands...")
        # Create brands
        brands_data = [
            {'name': 'Apple', 'slug': 'apple', 'description': 'Premium tech products'},
            {'name': 'Samsung', 'slug': 'samsung', 'description': 'Innovative electronics'},
            {'name': 'Sony', 'slug': 'sony', 'description': 'Audio and electronics'},
            {'name': 'Dell', 'slug': 'dell', 'description': 'Computer technology'},
            {'name': 'HP', 'slug': 'hp', 'description': 'Computing solutions'},
            {'name': 'Canon', 'slug': 'canon', 'description': 'Imaging solutions'},
        ]
        
        brands = []
        for brand_data in brands_data:
            brand = Brand(**brand_data, is_active=True)
            db.session.add(brand)
            brands.append(brand)
        
        db.session.flush()  # Get IDs
        
        print("Creating products...")
        # Sample products with enhanced data and multiple images
        products_data = [
            {
                'name': 'Samsung Galaxy A54 5G',
                'slug': 'samsung-galaxy-a54-5g',
                'description': 'Experience the latest Samsung smartphone with 128GB storage, 6GB RAM, and advanced triple camera system. Features include Super AMOLED display, 5000mAh battery, and 5G connectivity.',
                'short_description': 'Latest Samsung smartphone with 128GB storage, 6GB RAM, and triple camera system.',
                'price': Decimal('45000.00'),
                'original_price': Decimal('52000.00'),
                'sku': 'SAM-A54-128GB',
                'stock_quantity': 25,
                'weight': 0.202,
                'dimensions': '158.2 x 76.7 x 8.2 mm',
                'color': 'Awesome Black',
                'warranty_period': '1 Year',
                'category_id': categories[0].id,  # Smartphones
                'brand_id': brands[1].id,         # Samsung
                'is_active': True,
                'is_featured': True,
                'meta_title': 'Samsung Galaxy A54 5G - Premium Smartphone',
                'meta_description': 'Buy Samsung Galaxy A54 5G with 128GB storage and triple camera. Free delivery in Kenya.',
                'keywords': 'samsung, galaxy, smartphone, 5g, camera, android',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=800&fit=crop&crop=center&q=90',
                'additional_images': [
                    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=1200&h=900&fit=crop&crop=center&q=90'
                ]
            },
            {
                'name': 'iPhone 14 Pro',
                'slug': 'iphone-14-pro',
                'description': 'Apple iPhone 14 Pro with 128GB storage, A16 Bionic chip, Pro camera system with 48MP main camera, and Dynamic Island.',
                'short_description': 'Apple iPhone 14 Pro with 128GB storage, A16 Bionic chip, and Pro camera system.',
                'price': Decimal('125000.00'),
                'original_price': Decimal('135000.00'),
                'sku': 'APL-IP14P-128GB',
                'stock_quantity': 15,
                'weight': 0.206,
                'dimensions': '147.5 x 71.5 x 7.85 mm',
                'color': 'Deep Purple',
                'warranty_period': '1 Year',
                'category_id': categories[0].id,  # Smartphones
                'brand_id': brands[0].id,         # Apple
                'is_active': True,
                'is_featured': True,
                'meta_title': 'iPhone 14 Pro - Professional Photography',
                'meta_description': 'Buy iPhone 14 Pro with Pro camera system and A16 Bionic chip. Premium build quality.',
                'keywords': 'iphone, apple, smartphone, pro, camera, ios',
                'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800&h=800&fit=crop&crop=center&q=90',
                'additional_images': [
                    'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200&h=900&fit=crop&crop=center&q=90'
                ]
            },
            {
                'name': 'MacBook Air M2',
                'slug': 'macbook-air-m2',
                'description': 'Apple MacBook Air with M2 chip, 8GB unified memory, 256GB SSD storage. Perfect for work, creativity, and everyday tasks with all-day battery life.',
                'short_description': 'Apple MacBook Air with M2 chip, 8GB RAM, 256GB SSD. Perfect for work and creativity.',
                'price': Decimal('145000.00'),
                'original_price': Decimal('155000.00'),
                'sku': 'APL-MBA-M2-256GB',
                'stock_quantity': 12,
                'weight': 1.24,
                'dimensions': '304.1 x 215 x 11.3 mm',
                'color': 'Midnight',
                'warranty_period': '1 Year',
                'category_id': categories[1].id,  # Laptops
                'brand_id': brands[0].id,         # Apple
                'is_active': True,
                'is_featured': True,
                'meta_title': 'MacBook Air M2 - Ultra-portable Laptop',
                'meta_description': 'Buy MacBook Air with M2 chip for exceptional performance and battery life.',
                'keywords': 'macbook, air, m2, laptop, apple, portable',
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&h=800&fit=crop&crop=center&q=90',
                'additional_images': [
                    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=1200&h=900&fit=crop&crop=center&q=90'
                ]
            },
            {
                'name': 'Sony WH-1000XM4',
                'slug': 'sony-wh-1000xm4',
                'description': 'Industry-leading noise canceling wireless headphones with 30-hour battery life, touch sensor controls, and speak-to-chat technology.',
                'short_description': 'Premium wireless noise-canceling headphones with 30-hour battery life.',
                'price': Decimal('28000.00'),
                'original_price': Decimal('32000.00'),
                'sku': 'SNY-WH1000XM4',
                'stock_quantity': 30,
                'weight': 0.254,
                'dimensions': '254 x 203 x 76 mm',
                'color': 'Black',
                'warranty_period': '1 Year',
                'category_id': categories[2].id,  # Audio
                'brand_id': brands[2].id,         # Sony
                'is_active': True,
                'is_featured': True,
                'meta_title': 'Sony WH-1000XM4 - Premium Noise Canceling Headphones',
                'meta_description': 'Buy Sony WH-1000XM4 headphones with industry-leading noise cancellation.',
                'keywords': 'sony, headphones, noise canceling, wireless, audio',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=800&fit=crop&crop=center&q=90',
                'additional_images': [
                    'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=1200&h=900&fit=crop&crop=center&q=90'
                ]
            },
            {
                'name': 'iPad Air 5th Generation',
                'slug': 'ipad-air-5th-generation',
                'description': 'Apple iPad Air with M1 chip, 64GB storage, 10.9-inch Liquid Retina display, and compatibility with Apple Pencil and Magic Keyboard.',
                'short_description': 'Apple iPad Air with M1 chip, 64GB storage, and 10.9-inch display.',
                'price': Decimal('75000.00'),
                'original_price': Decimal('82000.00'),
                'sku': 'APL-IPAD-AIR5-64GB',
                'stock_quantity': 20,
                'weight': 0.461,
                'dimensions': '247.6 x 178.5 x 6.1 mm',
                'color': 'Space Gray',
                'warranty_period': '1 Year',
                'category_id': categories[3].id,  # Tablets
                'brand_id': brands[0].id,         # Apple
                'is_active': True,
                'is_featured': True,
                'meta_title': 'iPad Air 5th Gen - Powerful Tablet',
                'meta_description': 'Buy iPad Air with M1 chip for powerful performance in a portable design.',
                'keywords': 'ipad, air, tablet, apple, m1, portable',
                'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&h=800&fit=crop&crop=center&q=90',
                'additional_images': [
                    'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1200&h=900&fit=crop&crop=center&q=90'
                ]
            },
            {
                'name': 'Dell XPS 13',
                'slug': 'dell-xps-13',
                'description': 'Ultra-portable laptop with Intel Core i7 processor, 16GB RAM, 512GB SSD, and stunning 13.4-inch InfinityEdge display.',
                'short_description': 'Ultra-portable laptop with Intel i7 processor, 16GB RAM, and 512GB SSD.',
                'price': Decimal('135000.00'),
                'sku': 'DEL-XPS13-i7-512GB',
                'stock_quantity': 8,
                'weight': 1.27,
                'dimensions': '295.7 x 198.8 x 14.8 mm',
                'color': 'Platinum Silver',
                'warranty_period': '1 Year',
                'category_id': categories[1].id,  # Laptops
                'brand_id': brands[3].id,         # Dell
                'is_active': True,
                'is_featured': True,
                'meta_title': 'Dell XPS 13 - Premium Ultrabook',
                'meta_description': 'Buy Dell XPS 13 ultrabook with Intel i7 and premium build quality.',
                'keywords': 'dell, xps, laptop, ultrabook, intel, premium',
                'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800&h=800&fit=crop&crop=center&q=90',
                'additional_images': [
                    'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=1200&h=900&fit=crop&crop=center&q=90'
                ]
            },
            {
                'name': 'Canon EOS R6 Mark II',
                'slug': 'canon-eos-r6-mark-ii',
                'description': 'Professional mirrorless camera with 24.2MP full-frame sensor, 4K video recording, and advanced autofocus system.',
                'short_description': 'Professional mirrorless camera with 24.2MP sensor and 4K video recording.',
                'price': Decimal('285000.00'),
                'sku': 'CAN-EOSR6M2',
                'stock_quantity': 5,
                'weight': 0.588,
                'dimensions': '138.4 x 98.4 x 88.4 mm',
                'color': 'Black',
                'warranty_period': '2 Years',
                'category_id': categories[5].id,  # Cameras
                'brand_id': brands[5].id,         # Canon
                'is_active': True,
                'is_featured': True,
                'meta_title': 'Canon EOS R6 Mark II - Professional Camera',
                'meta_description': 'Buy Canon EOS R6 Mark II for professional photography and videography.',
                'keywords': 'canon, camera, mirrorless, professional, photography',
                'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&h=800&fit=crop&crop=center&q=90',
                'additional_images': [
                    'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200&h=900&fit=crop&crop=center&q=90',
                    'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1200&h=900&fit=crop&crop=center&q=90'
                ]
            },
            {
                'name': 'HP Spectre x360',
                'slug': 'hp-spectre-x360',
                'description': '2-in-1 convertible laptop with Intel Core i7, 16GB RAM, 1TB SSD, and 13.5-inch OLED touchscreen display.',
                'short_description': '2-in-1 convertible laptop with Intel i7, 16GB RAM, and OLED touchscreen.',
                'price': Decimal('165000.00'),
                'sku': 'HP-SPECX360-i7-1TB',
                'stock_quantity': 6,
                'weight': 1.36,
                'dimensions': '298 x 220 x 17 mm',
                'color': 'Nightfall Black',
                'warranty_period': '1 Year',
                'category_id': categories[1].id,  # Laptops
                'brand_id': brands[4].id,         # HP
                'is_active': True,
                'is_featured': False,
                'meta_title': 'HP Spectre x360 - Premium 2-in-1 Laptop',
                'meta_description': 'Buy HP Spectre x360 convertible laptop with OLED display.',
                'keywords': 'hp, spectre, laptop, 2-in-1, convertible, oled'
            }
        ]
        
        # Add products to database
        for product_data in products_data:
            # Extract additional images before creating product
            additional_images = product_data.pop('additional_images', [])
            
            product = Product(**product_data)
            db.session.add(product)
            db.session.flush()  # Get product ID
            
            # Add main product image
            main_image = ProductImage(
                product_id=product.id,
                image_url=product_data['image_url'],
                is_primary=True,
                sort_order=1,
                is_active=True,
                alt_text=f"{product.name} - Main image"
            )
            db.session.add(main_image)
            
            # Add additional images
            for i, img_url in enumerate(additional_images, 2):
                additional_image = ProductImage(
                    product_id=product.id,
                    image_url=img_url,
                    is_primary=False,
                    sort_order=i,
                    is_active=True,
                    alt_text=f"{product.name} - Image {i}"
                )
                db.session.add(additional_image)
        
        db.session.commit()
        
        print(f"Successfully added:")
        print(f"- {len(categories)} categories")
        print(f"- {len(brands)} brands") 
        print(f"- {len(products_data)} products")
        print(f"- Multiple images per product for detailed inspection")
        
        # Display added products
        print("\nFeatured products:")
        for product in Product.query.filter_by(is_featured=True).all():
            print(f"- {product.name}: KSh {product.price:,} (Stock: {product.stock_quantity})")

if __name__ == '__main__':
    seed_data()