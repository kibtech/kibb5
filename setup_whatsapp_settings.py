#!/usr/bin/env python3
"""
Setup WhatsApp Settings Script
This script sets up basic WhatsApp notification settings in the database.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import SystemSettings

def setup_whatsapp_settings():
    """Set up basic WhatsApp notification settings"""
    try:
        app = create_app('default')
        
        with app.app_context():
            print("🔧 Setting up WhatsApp notification settings...")
            
            # Define the WhatsApp settings to create
            whatsapp_settings = [
                {
                    'key': 'whatsapp_enabled',
                    'value': 'true',
                    'description': 'Enable/disable WhatsApp notifications',
                    'category': 'notifications',
                    'is_public': False
                },
                {
                    'key': 'admin_whatsapp_number',
                    'value': '254703843792',  # Default admin number
                    'description': 'Admin WhatsApp number for notifications',
                    'category': 'notifications',
                    'is_public': False
                },
                {
                    'key': 'whatsapp_api_url',
                    'value': '',  # Empty for now - will use fallback logging
                    'description': 'WhatsApp Business API URL',
                    'category': 'notifications',
                    'is_public': False
                },
                {
                    'key': 'whatsapp_token',
                    'value': '',  # Empty for now - will use fallback logging
                    'description': 'WhatsApp Business API token',
                    'category': 'notifications',
                    'is_public': False
                }
            ]
            
            # Create or update each setting
            for setting_data in whatsapp_settings:
                existing_setting = SystemSettings.query.filter_by(key=setting_data['key']).first()
                
                if existing_setting:
                    # Update existing setting
                    existing_setting.value = setting_data['value']
                    existing_setting.description = setting_data['description']
                    existing_setting.category = setting_data['category']
                    existing_setting.is_public = setting_data['is_public']
                    print(f"✅ Updated setting: {setting_data['key']}")
                else:
                    # Create new setting
                    new_setting = SystemSettings(**setting_data)
                    db.session.add(new_setting)
                    print(f"✅ Created setting: {setting_data['key']}")
            
            # Commit all changes
            db.session.commit()
            print("✅ WhatsApp settings setup completed successfully!")
            
            # Display current settings
            print("\n📱 Current WhatsApp Settings:")
            for setting in SystemSettings.query.filter_by(category='notifications').all():
                print(f"  • {setting.key}: {setting.value}")
            
            print("\n💡 Note: WhatsApp API URL and token are empty, so notifications will be logged to console instead of sent via WhatsApp.")
            print("   To enable actual WhatsApp sending, configure these values in the admin settings panel.")
            
    except Exception as e:
        print(f"❌ Error setting up WhatsApp settings: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = setup_whatsapp_settings()
    if success:
        print("\n🎯 WhatsApp settings are now configured!")
        print("   The system will log notifications to console until you configure the WhatsApp API.")
    else:
        print("\n❌ Failed to setup WhatsApp settings. Check the error above.")
        sys.exit(1) 