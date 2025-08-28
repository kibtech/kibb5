#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
import random
import string

def fix_referral_codes():
    """Generate referral codes for users who don't have them"""
    print("🔧 Fixing Referral Codes...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Find users without referral codes
            users_without_codes = User.query.filter_by(referral_code=None).all()
            
            if not users_without_codes:
                print("✅ All users already have referral codes")
                return True
            
            print(f"📝 Found {len(users_without_codes)} users without referral codes")
            
            for user in users_without_codes:
                # Generate a unique referral code
                while True:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    if not User.query.filter_by(referral_code=code).first():
                        user.referral_code = code
                        print(f"✅ Generated referral code {code} for user {user.email}")
                        break
            
            db.session.commit()
            print(f"✅ Successfully generated referral codes for {len(users_without_codes)} users")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing referral codes: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🚀 Referral Code Fix Tool")
    print("=" * 50)
    
    success = fix_referral_codes()
    
    if success:
        print("\n✅ Referral codes are now properly set up!")
        print("💡 Users should now see their referral codes in the dashboard.")
    else:
        print("\n❌ Failed to fix referral codes. Please check the error above.") 