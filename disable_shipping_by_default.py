#!/usr/bin/env python3
"""
Script to disable shipping fees by default and set up shipping settings
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app import create_app
from app.models import db, SystemSettings

def setup_shipping_settings():
    """Set up shipping settings with shipping disabled by default"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🚀 Setting up shipping settings...")
            
            # Create or update shipping enabled setting (disabled by default)
            shipping_enabled_setting = db.session.query(SystemSettings).filter_by(key='shipping_enabled').first()
            if shipping_enabled_setting:
                shipping_enabled_setting.value = 'false'
                print("✅ Updated shipping_enabled setting to disabled")
            else:
                shipping_enabled_setting = SystemSettings(
                    key='shipping_enabled',
                    value='false',
                    description='Enable or disable shipping fees for e-commerce orders',
                    category='shipping'
                )
                db.session.add(shipping_enabled_setting)
                print("✅ Created shipping_enabled setting (disabled)")
            
            # Create or update shipping fee setting
            shipping_fee_setting = db.session.query(SystemSettings).filter_by(key='ecommerce_shipping_fee').first()
            if shipping_fee_setting:
                print(f"✅ Shipping fee setting exists: KSh {shipping_fee_setting.value}")
            else:
                shipping_fee_setting = SystemSettings(
                    key='ecommerce_shipping_fee',
                    value='200',
                    description='Standard shipping fee for e-commerce orders (in KSh)',
                    category='shipping'
                )
                db.session.add(shipping_fee_setting)
                print("✅ Created shipping fee setting: KSh 200")
            
            # Create or update free shipping threshold setting
            free_shipping_setting = db.session.query(SystemSettings).filter_by(key='free_shipping_threshold').first()
            if free_shipping_setting:
                print(f"✅ Free shipping threshold exists: KSh {free_shipping_setting.value}")
            else:
                free_shipping_setting = SystemSettings(
                    key='free_shipping_threshold',
                    value='5000',
                    description='Order amount above which shipping is free (in KSh)',
                    category='shipping'
                )
                db.session.add(free_shipping_setting)
                print("✅ Created free shipping threshold: KSh 5000")
            
            db.session.commit()
            
            print("\n🎉 Shipping settings configured successfully!")
            print("\n📝 Current Configuration:")
            print(f"   • Shipping Enabled: {shipping_enabled_setting.value}")
            print(f"   • Shipping Fee: KSh {shipping_fee_setting.value}")
            print(f"   • Free Shipping Threshold: KSh {free_shipping_setting.value}")
            print("\n💡 To enable shipping:")
            print("   1. Go to Admin Portal")
            print("   2. Navigate to Settings > Shipping")
            print("   3. Toggle 'Enable Shipping Fees' to ON")
            print("   4. Configure your shipping fee and free shipping threshold")
            
        except Exception as e:
            print(f"❌ Error setting up shipping settings: {e}")
            db.session.rollback()
            return False
        
    return True

if __name__ == "__main__":
    print("============================================================")
    print("          Shipping Settings Configuration")
    print("============================================================")
    
    success = setup_shipping_settings()
    if success:
        print("\n✅ Configuration completed successfully!")
    else:
        print("\n❌ Configuration failed!")
        sys.exit(1)