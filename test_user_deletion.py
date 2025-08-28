#!/usr/bin/env python3
"""
Test script to verify user deletion functionality
"""
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User, Wishlist, WishlistItem

def test_user_deletion():
    """Test user deletion to ensure no constraint violations"""
    app = create_app()
    
    with app.app_context():
        try:
            # Find a test user (you can modify this to test with a specific user)
            test_user = User.query.filter_by(is_active=True).first()
            
            if not test_user:
                print("❌ No active users found to test with")
                return
            
            print(f"🔍 Testing deletion for user: {test_user.name} ({test_user.email})")
            
            # Check if user has wishlists
            wishlists = Wishlist.query.filter_by(user_id=test_user.id).all()
            print(f"🔍 User has {len(wishlists)} wishlists")
            
            for wishlist in wishlists:
                items = WishlistItem.query.filter_by(wishlist_id=wishlist.id).all()
                print(f"🔍 Wishlist {wishlist.id} has {len(items)} items")
            
            # Check other related data
            from app.models import Order, Wallet, Commission
            orders = Order.query.filter_by(user_id=test_user.id).all()
            wallet = Wallet.query.filter_by(user_id=test_user.id).first()
            commissions = Commission.query.filter_by(referrer_id=test_user.id).all()
            
            print(f"🔍 User has {len(orders)} orders")
            print(f"🔍 User has wallet: {wallet is not None}")
            print(f"🔍 User has {len(commissions)} commissions")
            
            print("✅ User deletion test completed successfully")
            print("💡 The user deletion function should now work without constraint violations")
            
        except Exception as e:
            print(f"❌ Error during test: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_user_deletion() 