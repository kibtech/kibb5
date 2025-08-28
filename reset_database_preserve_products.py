#!/usr/bin/env python3
"""
Database Reset Script for KIBTECH ONLINE SERVICES
This script resets the database but preserves all products and categories
Run with: python reset_database_preserve_products.py
"""

import os
import sys
from app import create_app, db
from app.models import Product, Category, Brand, ProductImage, User, Order, Cart, Wishlist, Wallet, AdminUser

def backup_products():
    """Backup all products, categories, and brands"""
    print("📦 Backing up products, categories, and brands...")
    
    # Backup categories
    categories = Category.query.all()
    categories_data = []
    for cat in categories:
        categories_data.append({
            'name': cat.name,
            'slug': cat.slug,
            'description': cat.description,
            'is_active': cat.is_active
        })
    
    # Backup brands
    brands = Brand.query.all()
    brands_data = []
    for brand in brands:
        brands_data.append({
            'name': brand.name,
            'slug': brand.slug,
            'description': brand.description,
            'is_active': brand.is_active
        })
    
    # Backup products with images
    products = Product.query.all()
    products_data = []
    for product in products:
        # Get product images
        images = ProductImage.query.filter_by(product_id=product.id).all()
        image_data = []
        for img in images:
            image_data.append({
                'image_url': img.image_url,
                'is_primary': img.is_primary,
                'sort_order': img.sort_order,
                'is_active': img.is_active,
                'alt_text': img.alt_text
            })
        
        products_data.append({
            'name': product.name,
            'slug': product.slug,
            'description': product.description,
            'short_description': product.short_description,
            'price': product.price,
            'original_price': product.original_price,
            'sku': product.sku,
            'stock_quantity': product.stock_quantity,
            'weight': product.weight,
            'dimensions': product.dimensions,
            'color': product.color,
            'warranty_period': product.warranty_period,
            'is_active': product.is_active,
            'is_featured': product.is_featured,
            'meta_title': product.meta_title,
            'meta_description': product.meta_description,
            'keywords': product.keywords,
            'category_slug': product.category.slug if product.category else None,
            'brand_slug': product.brand.slug if product.brand else None,
            'images': image_data
        })
    
    return {
        'categories': categories_data,
        'brands': brands_data,
        'products': products_data
    }

def restore_products(backup_data):
    """Restore products, categories, and brands from backup"""
    print("🔄 Restoring products, categories, and brands...")
    
    # Restore categories
    categories_map = {}
    for cat_data in backup_data['categories']:
        category = Category(**cat_data)
        db.session.add(category)
        db.session.flush()
        categories_map[cat_data['slug']] = category
        print(f"✅ Restored category: {category.name}")
    
    # Restore brands
    brands_map = {}
    for brand_data in backup_data['brands']:
        brand = Brand(**brand_data)
        db.session.add(brand)
        db.session.flush()
        brands_map[brand_data['slug']] = brand
        print(f"✅ Restored brand: {brand.name}")
    
    # Restore products
    for product_data in backup_data['products']:
        # Extract images and category/brand slugs
        images = product_data.pop('images', [])
        category_slug = product_data.pop('category_slug')
        brand_slug = product_data.pop('brand_slug')
        
        # Set category and brand IDs
        if category_slug and category_slug in categories_map:
            product_data['category_id'] = categories_map[category_slug].id
        if brand_slug and brand_slug in brands_map:
            product_data['brand_id'] = brands_map[brand_slug].id
        
        # Create product
        product = Product(**product_data)
        db.session.add(product)
        db.session.flush()
        
        # Restore product images
        for img_data in images:
            img_data['product_id'] = product.id
            image = ProductImage(**img_data)
            db.session.add(image)
        
        print(f"✅ Restored product: {product.name}")
    
    db.session.commit()

def reset_database_preserve_products():
    """Reset database while preserving all products"""
    print("🔄 Resetting KIBTECH database while preserving products...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Backup products
            backup_data = backup_products()
            
            print(f"📦 Backed up {len(backup_data['categories'])} categories")
            print(f"📦 Backed up {len(backup_data['brands'])} brands")
            print(f"📦 Backed up {len(backup_data['products'])} products")
            
            # Drop all tables
            print("🗑️ Dropping all tables...")
            db.drop_all()
            
            # Recreate all tables
            print("📋 Recreating database tables...")
            db.create_all()
            
            # Restore products
            restore_products(backup_data)
            
            # Create default admin
            from auto_seed_products import create_default_admin
            create_default_admin()
            
            print("\n✅ Database reset completed successfully!")
            print("🎉 All products have been preserved and are available!")
            print(f"📦 Total products available: {Product.query.count()}")
            print(f"🏷️ Total categories: {Category.query.count()}")
            print(f"🏢 Total brands: {Brand.query.count()}")
            
        except Exception as e:
            print(f"❌ Error during database reset: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    reset_database_preserve_products() 