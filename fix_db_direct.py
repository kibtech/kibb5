#!/usr/bin/env python3
"""
Fix database directly using Flask app context
"""

from app import create_app, db
from sqlalchemy import text

def fix_database():
    """Add missing email_verified column using Flask app context"""
    print("🔧 Fixing Database Schema")
    print("=" * 40)
    
    try:
        print("Creating Flask app...")
        app = create_app()
        print("✅ Flask app created successfully")
        
        with app.app_context():
            print("✅ Flask app context created")
            
            # Check if column exists
            try:
                print("Checking if email_verified column exists...")
                result = db.session.execute(text("SELECT email_verified FROM users LIMIT 1"))
                print("✅ email_verified column already exists")
                return
            except Exception as e:
                print(f"Error checking column: {str(e)}")
                if "column users.email_verified does not exist" in str(e) or "column \"email_verified\" does not exist" in str(e):
                    print("❌ email_verified column is missing - adding it now...")
                else:
                    print(f"❌ Error checking column: {str(e)}")
                    return
            
            # Add the missing column
            try:
                print("🔧 Adding email_verified column to users table...")
                db.session.execute(text("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE"))
                db.session.commit()
                print("✅ email_verified column added successfully")
                
                # Verify the column was added
                result = db.session.execute(text("SELECT email_verified FROM users LIMIT 1"))
                print("✅ Column verification successful")
                
                print("\n🎉 Database schema fixed successfully!")
                
            except Exception as e:
                print(f"❌ Error adding column: {str(e)}")
                db.session.rollback()
                import traceback
                traceback.print_exc()
    
    except Exception as e:
        print(f"❌ App creation error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting database fix...")
    fix_database()
    print("Script completed.") 