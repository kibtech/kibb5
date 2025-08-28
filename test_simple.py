#!/usr/bin/env python3
"""
Simple test to check Flask app
"""

print("🚀 Starting simple test...")

try:
    from app import create_app
    print("✅ App import successful")
    
    app = create_app()
    print("✅ App creation successful")
    
    with app.app_context():
        print("✅ App context successful")
        
        from app import db
        print("✅ Database import successful")
        
        # Try to create tables
        try:
            db.create_all()
            print("✅ Database tables created")
        except Exception as e:
            print(f"❌ Database creation failed: {e}")
            
except Exception as e:
    print(f"❌ Import failed: {e}")

print("�� Test completed") 