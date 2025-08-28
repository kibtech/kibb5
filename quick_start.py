#!/usr/bin/env python3
"""
Quick Start Script for KIBTECH ONLINE SERVICES
=============================================

This script quickly checks the database status and starts the application
without trying to recreate existing tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import AdminUser, AdminRole, User, Product, Category, Brand
from sqlalchemy import text

def check_database_ready():
    """Quick check if database is ready"""
    print("🔍 Quick database check...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test connection
            result = db.session.execute(text('SELECT 1'))
            
            # Quick counts
            admin_count = AdminUser.query.count()
            category_count = Category.query.count()
            product_count = Product.query.count()
            
            print(f"✅ Database ready! Admin: {admin_count}, Categories: {category_count}, Products: {product_count}")
            return True
            
        except Exception as e:
            print(f"❌ Database not ready: {str(e)}")
            return False

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    
    try:
        from run import app
        print("✅ Backend starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Failed to start backend: {str(e)}")

def main():
    """Main function"""
    print("🚀 KIBTECH Quick Start")
    print("=" * 30)
    
    if not check_database_ready():
        print("❌ Database not ready. Please run fix_database_and_admin.py first.")
        return False
    
    print("\n✅ Everything is ready!")
    print("📋 Admin Login:")
    print("   Email: kibtechc@gmail.com")
    print("   Password: admin123")
    print("   Username: kibtech_admin")
    
    start_backend()
    return True

if __name__ == "__main__":
    main() 