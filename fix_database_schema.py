#!/usr/bin/env python3
"""
Fix Database Schema - Update admin_users table to match current model
"""
import os
import sys
from datetime import datetime
from app import create_app, db

def fix_database_schema():
    """Drop and recreate all tables to match current models"""
    print("🔧 Fixing database schema...")
    
    try:
        app = create_app()
        
        with app.app_context():
            print("📋 Dropping all existing tables...")
            db.drop_all()
            
            print("🏗️  Creating tables with current schema...")
            db.create_all()
            
            print("✅ Database schema updated successfully!")
            print("📋 All tables recreated with current model structure")
            
            return True
            
    except Exception as e:
        print(f"❌ Error fixing database schema: {str(e)}")
        return False

if __name__ == '__main__':
    success = fix_database_schema()
    if success:
        print("\n🎉 Database schema fix completed!")
        print("💡 Now run: python setup_admin.py")
    else:
        print("\n❌ Failed to fix database schema")
        sys.exit(1)