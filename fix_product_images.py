#!/usr/bin/env python3
"""
Fix product image_url column to support base64 images
"""

from app import create_app, db
from sqlalchemy import text
import os

def fix_product_images():
    """Change product image_url from VARCHAR(500) to TEXT"""
    try:
        app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        
        with app.app_context():
            print("🔧 Fixing product image_url column size...")
            print("=" * 50)
            
            try:
                # Change the column type from VARCHAR(500) to TEXT for products table
                db.session.execute(text('ALTER TABLE products ALTER COLUMN image_url TYPE TEXT'))
                
                # Also fix ProductImage table
                db.session.execute(text('ALTER TABLE product_images ALTER COLUMN image_url TYPE TEXT'))
                
                db.session.commit()
                
                print("✅ Successfully changed products.image_url column to TEXT type")
                print("✅ Successfully changed product_images.image_url column to TEXT type")
                print("📸 Base64 images can now be stored in product image fields")
                
                return True
                
            except Exception as e:
                print(f"❌ Error updating image_url columns: {e}")
                db.session.rollback()
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Fixing product image columns for base64 support...")
    
    if fix_product_images():
        print("\n✅ Database update completed successfully!")
        print("🎉 You can now upload large product images that will be stored as base64!")
    else:
        print("\n❌ Database update failed!")
        print("Please check the error messages above.")