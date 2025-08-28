#!/usr/bin/env python3
"""
Fix Remaining Referral Relationships
This script specifically addresses the 11 users who have referral codes
but no referral relationships established.
"""

import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_remaining_referral_relationships():
    """Fix the remaining users with referral codes but no referral relationships"""
    
    app = create_app()
    
    with app.app_context():
        logger.info("🔧 Fixing remaining referral relationships...")
        
        # Find users with referral codes but no referred_by_id
        users_with_referral_codes = User.query.filter(
            User.referral_code.isnot(None),
            User.referral_code != '',
            User.referred_by_id.is_(None)
        ).all()
        
        logger.info(f"Found {len(users_with_referral_codes)} users with referral codes but no referral relationship")
        
        fixed_count = 0
        for user in users_with_referral_codes:
            logger.info(f"Processing user: {user.email} with referral code: {user.referral_code}")
            
            # Find the user who has this referral code
            referrer = User.query.filter_by(referral_code=user.referral_code).first()
            
            if referrer and referrer.id != user.id:
                user.referred_by_id = referrer.id
                fixed_count += 1
                logger.info(f"✅ Fixed: {user.email} -> {referrer.email}")
            else:
                logger.warning(f"⚠️  Could not find referrer for {user.email} with code {user.referral_code}")
        
        # Commit all changes
        db.session.commit()
        
        logger.info(f"✅ Fixed {fixed_count} referral relationships")
        
        # Verify the fix
        remaining_issues = User.query.filter(
            User.referral_code.isnot(None),
            User.referral_code != '',
            User.referred_by_id.is_(None)
        ).count()
        
        logger.info(f"Remaining users with referral issues: {remaining_issues}")
        
        if remaining_issues == 0:
            logger.info("🎉 All referral relationships are now properly established!")
        else:
            logger.warning(f"⚠️  {remaining_issues} users still have referral issues")
        
        return fixed_count, remaining_issues

if __name__ == "__main__":
    try:
        fixed, remaining = fix_remaining_referral_relationships()
        
        print(f"\n🎯 REFERRAL RELATIONSHIP FIX RESULTS:")
        print(f"✅ Fixed: {fixed} referral relationships")
        print(f"⚠️  Remaining issues: {remaining}")
        
        if remaining == 0:
            print("\n🎉 SUCCESS! All referral relationships are now properly established!")
            print("Your referral system should work perfectly now!")
        else:
            print(f"\n⚠️  There are still {remaining} users with referral issues")
            print("These might be users with invalid or duplicate referral codes")
        
    except Exception as e:
        logger.error(f"Failed to fix remaining referral relationships: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 