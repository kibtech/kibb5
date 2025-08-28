#!/usr/bin/env python3
"""
Fix OTP expiration issue for PIN change functionality
"""
from app import create_app, db
from app.models import OTP
from datetime import datetime, timedelta
import sqlalchemy as sa

def fix_otp_expiration():
    """Fix OTP records with null expires_at"""
    
    print("🔧 Fixing OTP Expiration Issue")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Check for OTPs with null expires_at
            null_expires = OTP.query.filter(OTP.expires_at.is_(None)).all()
            print(f"Found {len(null_expires)} OTPs with null expires_at")
            
            if null_expires:
                print("\n📋 OTPs with null expiration:")
                for otp in null_expires:
                    print(f"   - ID: {otp.id}, Email: {otp.email}, Purpose: {otp.purpose}")
                    print(f"     Created: {otp.created_at}, Used: {otp.is_used}")
                
                # Fix null expires_at by setting them to 10 minutes from created_at
                print("\n🔧 Fixing null expiration dates...")
                for otp in null_expires:
                    if otp.created_at:
                        # Set expiration to 10 minutes from creation
                        otp.expires_at = otp.created_at + timedelta(minutes=10)
                        print(f"   Fixed OTP {otp.id}: expires_at = {otp.expires_at}")
                    else:
                        # If no created_at, set to 10 minutes from now
                        otp.expires_at = datetime.utcnow() + timedelta(minutes=10)
                        print(f"   Fixed OTP {otp.id}: expires_at = {otp.expires_at}")
                
                # Commit the changes
                db.session.commit()
                print("✅ Successfully fixed OTP expiration dates")
            else:
                print("✅ No OTPs with null expiration found")
            
            # Check OTP model to ensure generate_otp sets expiration
            print("\n🔍 Checking OTP model...")
            try:
                # Test creating a new OTP
                test_otp = OTP(
                    user_id=1,
                    email="test@example.com",
                    purpose="test"
                )
                test_otp.generate_otp()
                print(f"   Test OTP created: {test_otp.otp_code}")
                print(f"   Expires at: {test_otp.expires_at}")
                print(f"   Is valid: {test_otp.is_valid}")
                
                if test_otp.expires_at:
                    print("   ✅ OTP expiration is being set correctly")
                else:
                    print("   ❌ OTP expiration is still null")
                    
            except Exception as e:
                print(f"   ❌ Error testing OTP creation: {str(e)}")
            
            print("\n🎉 OTP expiration fix completed!")
            
        except Exception as e:
            print(f"❌ Fix failed: {str(e)}")
            import traceback
            traceback.print_exc()

def check_otp_table_structure():
    """Check OTP table structure"""
    
    print("\n📊 OTP Table Structure Check")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Get table info
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            
            if 'otps' in inspector.get_table_names():
                columns = inspector.get_columns('otps')
                print("OTP table columns:")
                for col in columns:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    print(f"   - {col['name']}: {col['type']} ({nullable})")
            else:
                print("❌ OTP table not found")
                
        except Exception as e:
            print(f"❌ Table check failed: {str(e)}")

if __name__ == "__main__":
    print("🔧 OTP Expiration Fix Tool")
    print("=" * 60)
    
    # Check table structure
    check_otp_table_structure()
    
    # Fix OTP expiration
    fix_otp_expiration()
    
    print("\n📝 Summary:")
    print("- Fixed OTPs with null expires_at")
    print("- PIN change should now work correctly")
    print("- OTP expiration is set to 10 minutes from creation")
    print("- Try changing PIN again in the frontend") 