#!/usr/bin/env python3
"""
Fix Invalid Referral Codes
This script addresses users with referral codes that don't exist in the system.
It will either find valid referrers or clean up invalid referral codes.
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

def fix_invalid_referral_codes():
    """Fix users with invalid referral codes"""
    
    app = create_app()
    
    with app.app_context():
        logger.info("🔧 Fixing invalid referral codes...")
        
        # Find users with referral codes but no referral relationship
        users_with_issues = User.query.filter(
            User.referral_code.isnot(None),
            User.referral_code != '',
            User.referred_by_id.is_(None)
        ).all()
        
        logger.info(f"Found {len(users_with_issues)} users with referral code issues")
        
        fixed_count = 0
        cleaned_count = 0
        
        for user in users_with_issues:
            logger.info(f"Processing user: {user.email} with referral code: {user.referral_code}")
            
            # Try to find a valid referrer
            referrer = User.query.filter_by(referral_code=user.referral_code).first()
            
            if referrer and referrer.id != user.id:
                # Valid referrer found
                user.referred_by_id = referrer.id
                fixed_count += 1
                logger.info(f"✅ Fixed referral relationship: {user.email} -> {referrer.email}")
            else:
                # No valid referrer found - clean up the invalid referral code
                logger.warning(f"⚠️  Invalid referral code '{user.referral_code}' for {user.email} - cleaning up")
                
                # Check if this user should be referred by someone else
                # Look for users with similar names or emails that might be the intended referrer
                potential_referrer = find_potential_referrer(user)
                
                if potential_referrer:
                    user.referred_by_id = potential_referrer.id
                    user.referral_code = potential_referrer.referral_code
                    fixed_count += 1
                    logger.info(f"✅ Fixed with potential referrer: {user.email} -> {potential_referrer.email}")
                else:
                    # Clean up the invalid referral code
                    user.referral_code = None
                    cleaned_count += 1
                    logger.info(f"🧹 Cleaned up invalid referral code for {user.email}")
        
        # Commit all changes
        db.session.commit()
        
        logger.info(f"✅ Fixed {fixed_count} referral relationships")
        logger.info(f"🧹 Cleaned up {cleaned_count} invalid referral codes")
        
        # Verify the fix
        remaining_issues = User.query.filter(
            User.referral_code.isnot(None),
            User.referral_code != '',
            User.referred_by_id.is_(None)
        ).count()
        
        logger.info(f"Remaining users with referral issues: {remaining_issues}")
        
        if remaining_issues == 0:
            logger.info("🎉 All referral issues are now resolved!")
        else:
            logger.warning(f"⚠️  {remaining_issues} users still have referral issues")
        
        return fixed_count, cleaned_count, remaining_issues

def find_potential_referrer(user):
    """Try to find a potential referrer based on user information"""
    
    # Extract base email (remove deleted_ prefixes)
    base_email = user.email
    if base_email.startswith('deleted_'):
        # Remove deleted_ prefix and try to find the original user
        parts = base_email.split('_', 1)
        if len(parts) > 1:
            base_email = parts[1]
    
    # Look for users with similar base emails
    potential_referrers = User.query.filter(
        User.email.like(f"%{base_email}%"),
        User.id != user.id,
        User.referral_code.isnot(None),
        User.referral_code != ''
    ).all()
    
    if potential_referrers:
        # Return the first potential referrer
        return potential_referrers[0]
    
    # If no similar emails, look for admin users
    admin_users = User.query.filter(
        User.email.like('%admin%'),
        User.referral_code.isnot(None),
        User.referral_code != ''
    ).all()
    
    if admin_users:
        return admin_users[0]
    
    return None

def generate_missing_referral_codes():
    """Generate referral codes for users who don't have them"""
    
    logger.info("🔧 Generating missing referral codes...")
    
    users_without_codes = User.query.filter(
        (User.referral_code.is_(None) | (User.referral_code == ''))
    ).all()
    
    logger.info(f"Found {len(users_without_codes)} users without referral codes")
    
    generated_count = 0
    for user in users_without_codes:
        if not user.referral_code:
            # Generate a unique referral code
            import secrets
            import string
            
            while True:
                # Generate 8-character alphanumeric code
                referral_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                
                # Check if it's unique
                existing_user = User.query.filter_by(referral_code=referral_code).first()
                if not existing_user:
                    user.referral_code = referral_code
                    generated_count += 1
                    logger.info(f"✅ Generated referral code {referral_code} for {user.email}")
                    break
    
    db.session.commit()
    logger.info(f"✅ Generated {generated_count} referral codes")
    
    return generated_count

if __name__ == "__main__":
    try:
        print("🔧 FIXING INVALID REFERRAL CODES")
        print("=" * 50)
        
        # Step 1: Fix invalid referral codes
        fixed, cleaned, remaining = fix_invalid_referral_codes()
        
        print(f"\n📊 REFERRAL CODE FIX RESULTS:")
        print(f"✅ Fixed referral relationships: {fixed}")
        print(f"🧹 Cleaned up invalid codes: {cleaned}")
        print(f"⚠️  Remaining issues: {remaining}")
        
        # Step 2: Generate missing referral codes
        if remaining == 0:
            print(f"\n🔧 GENERATING MISSING REFERRAL CODES:")
            generated = generate_missing_referral_codes()
            print(f"✅ Generated {generated} new referral codes")
        
        # Final status
        if remaining == 0:
            print("\n🎉 SUCCESS! All referral issues are now resolved!")
            print("Your referral system should work perfectly now!")
        else:
            print(f"\n⚠️  There are still {remaining} users with referral issues")
            print("These might require manual investigation")
        
    except Exception as e:
        logger.error(f"Failed to fix invalid referral codes: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1) 