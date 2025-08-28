#!/usr/bin/env python3
"""
Setup Commission Rates
=====================
Set up different commission rates for ecommerce products (3%) and cyber services (20%).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import SystemSettings, Commission
from decimal import Decimal

def setup_commission_rates():
    """Set up commission rates in system settings"""
    print("🔧 Setting up commission rates...")
    
    try:
        app = create_app()
        with app.app_context():
            # Define commission rates
            commission_settings = [
                {
                    'key': 'ecommerce_commission_rate',
                    'value': '3.0',
                    'description': 'Commission rate for ecommerce product referrals (%)',
                    'category': 'commission'
                },
                {
                    'key': 'cyber_services_commission_rate', 
                    'value': '20.0',
                    'description': 'Commission rate for cyber service referrals (%)',
                    'category': 'commission'
                },
                {
                    'key': 'default_commission_rate',
                    'value': '3.0',
                    'description': 'Default commission rate for referrals (%)',
                    'category': 'commission'
                }
            ]
            
            # Add or update settings
            for setting_data in commission_settings:
                existing_setting = db.session.query(SystemSettings).filter_by(key=setting_data['key']).first()
                
                if existing_setting:
                    existing_setting.value = setting_data['value']
                    existing_setting.description = setting_data['description']
                    print(f"   ✅ Updated {setting_data['key']}: {setting_data['value']}%")
                else:
                    new_setting = SystemSettings(
                        key=setting_data['key'],
                        value=setting_data['value'],
                        description=setting_data['description'],
                        category=setting_data['category']
                    )
                    db.session.add(new_setting)
                    print(f"   ✅ Added {setting_data['key']}: {setting_data['value']}%")
            
            db.session.commit()
            print("   ✅ Commission rates configured successfully!")
            
    except Exception as e:
        print(f"   ❌ Error setting up commission rates: {e}")
        db.session.rollback()

def get_commission_rate(order_type='ecommerce'):
    """Get commission rate for a specific order type"""
    try:
        app = create_app()
        with app.app_context():
            if order_type == 'cyber_services':
                setting = db.session.query(SystemSettings).filter_by(key='cyber_services_commission_rate').first()
            else:
                setting = db.session.query(SystemSettings).filter_by(key='ecommerce_commission_rate').first()
            
            if setting:
                return float(setting.value) / 100.0  # Convert percentage to decimal
            else:
                # Fallback to default
                default_setting = db.session.query(SystemSettings).filter_by(key='default_commission_rate').first()
                return float(default_setting.value) / 100.0 if default_setting else 0.03  # 3% default
    except Exception as e:
        print(f"Error getting commission rate: {e}")
        return 0.03  # 3% fallback

def test_commission_rates():
    """Test the commission rate configuration"""
    print("\n🧪 Testing commission rates...")
    
    try:
        app = create_app()
        with app.app_context():
            # Test ecommerce commission rate
            ecommerce_rate = get_commission_rate('ecommerce')
            print(f"   📦 Ecommerce commission rate: {ecommerce_rate * 100}%")
            
            # Test cyber services commission rate
            cyber_rate = get_commission_rate('cyber_services')
            print(f"   🔒 Cyber services commission rate: {cyber_rate * 100}%")
            
            # Test commission calculations
            test_amount = 1000.0
            
            ecommerce_commission = Decimal(str(test_amount * ecommerce_rate))
            cyber_commission = Decimal(str(test_amount * cyber_rate))
            
            print(f"   💰 Test commission for KSh {test_amount}:")
            print(f"      - Ecommerce: KSh {ecommerce_commission}")
            print(f"      - Cyber Services: KSh {cyber_commission}")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Error testing commission rates: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Setting up Commission Rates...")
    print("=" * 50)
    
    # Setup commission rates
    setup_commission_rates()
    
    # Test the configuration
    if test_commission_rates():
        print("\n✅ Commission rates setup completed successfully!")
        print("\n📋 Summary:")
        print("   📦 Ecommerce Products: 3% commission")
        print("   🔒 Cyber Services: 20% commission")
        print("   💡 Default: 3% commission")
    else:
        print("\n❌ Commission rates setup failed!")

if __name__ == "__main__":
    main() 