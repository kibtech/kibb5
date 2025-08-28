#!/usr/bin/env python3
"""
Fix wishlist count mismatch issue
"""
from app import create_app, db
from app.models import User, Wishlist, WishlistItem, Product

def diagnose_wishlist_issue():
    """Diagnose wishlist count mismatch"""
    
    print("🔍 Diagnosing Wishlist Count Issue")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Get all users with wishlists
            users = User.query.all()
            
            for user in users:
                print(f"\n👤 User: {user.name} ({user.email})")
                
                # Get user's wishlist
                wishlist = Wishlist.query.filter_by(user_id=user.id).first()
                
                if not wishlist:
                    print("   ❌ No wishlist found")
                    continue
                
                # Count items in wishlist
                item_count = wishlist.items.count()
                print(f"   📊 Wishlist ID: {wishlist.id}")
                print(f"   📊 Item count: {item_count}")
                
                # Get actual items
                items = wishlist.items.all()
                print(f"   📋 Actual items: {len(items)}")
                
                # Check for orphaned items
                orphaned_items = WishlistItem.query.filter_by(wishlist_id=wishlist.id).all()
                print(f"   🔗 Database items: {len(orphaned_items)}")
                
                # Check if products exist
                valid_items = 0
                for item in items:
                    product = Product.query.get(item.product_id)
                    if product and product.is_active:
                        valid_items += 1
                    else:
                        print(f"      ⚠️  Invalid product ID: {item.product_id}")
                
                print(f"   ✅ Valid products: {valid_items}")
                
                # Check for orphaned wishlist items
                orphaned_wishlist_items = db.session.query(WishlistItem).filter(
                    ~WishlistItem.wishlist_id.in_([w.id for w in Wishlist.query.all()])
                ).all()
                
                if orphaned_wishlist_items:
                    print(f"   🗑️  Orphaned wishlist items: {len(orphaned_wishlist_items)}")
                    for item in orphaned_wishlist_items:
                        print(f"      - Item ID: {item.id}, Product ID: {item.product_id}")
                
                # Check for duplicate items
                from sqlalchemy import func
                duplicates = db.session.query(
                    WishlistItem.wishlist_id,
                    WishlistItem.product_id,
                    func.count(WishlistItem.id).label('count')
                ).group_by(
                    WishlistItem.wishlist_id,
                    WishlistItem.product_id
                ).having(func.count(WishlistItem.id) > 1).all()
                
                if duplicates:
                    print(f"   🔄 Duplicate items found: {len(duplicates)}")
                    for dup in duplicates:
                        print(f"      - Wishlist {dup.wishlist_id}, Product {dup.product_id}: {dup.count} times")
                
                print()
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

def fix_wishlist_issues():
    """Fix wishlist count issues"""
    
    print("\n🔧 Fixing Wishlist Issues")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # 1. Remove orphaned wishlist items
            print("1. Removing orphaned wishlist items...")
            orphaned_items = db.session.query(WishlistItem).filter(
                ~WishlistItem.wishlist_id.in_([w.id for w in Wishlist.query.all()])
            ).all()
            
            for item in orphaned_items:
                db.session.delete(item)
            
            print(f"   Removed {len(orphaned_items)} orphaned items")
            
            # 2. Remove duplicate items
            print("2. Removing duplicate items...")
            from sqlalchemy import func
            
            duplicates = db.session.query(
                WishlistItem.wishlist_id,
                WishlistItem.product_id,
                func.count(WishlistItem.id).label('count')
            ).group_by(
                WishlistItem.wishlist_id,
                WishlistItem.product_id
            ).having(func.count(WishlistItem.id) > 1).all()
            
            for dup in duplicates:
                # Keep the first item, delete the rest
                items_to_keep = WishlistItem.query.filter_by(
                    wishlist_id=dup.wishlist_id,
                    product_id=dup.product_id
                ).order_by(WishlistItem.id).first()
                
                if items_to_keep:
                    items_to_delete = WishlistItem.query.filter_by(
                        wishlist_id=dup.wishlist_id,
                        product_id=dup.product_id
                    ).filter(WishlistItem.id != items_to_keep.id).all()
                    
                    for item in items_to_delete:
                        db.session.delete(item)
            
            print(f"   Removed duplicates for {len(duplicates)} product-wishlist combinations")
            
            # 3. Remove items with invalid products
            print("3. Removing items with invalid products...")
            invalid_items = []
            
            for wishlist_item in WishlistItem.query.all():
                product = Product.query.get(wishlist_item.product_id)
                if not product or not product.is_active:
                    invalid_items.append(wishlist_item)
            
            for item in invalid_items:
                db.session.delete(item)
            
            print(f"   Removed {len(invalid_items)} items with invalid products")
            
            # 4. Commit changes
            db.session.commit()
            print("✅ All fixes applied successfully!")
            
            # 5. Verify fixes
            print("\n🔍 Verifying fixes...")
            diagnose_wishlist_issue()
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during fix: {str(e)}")
            import traceback
            traceback.print_exc()

def test_wishlist_count_api():
    """Test the wishlist count API"""
    
    print("\n🧪 Testing Wishlist Count API")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Get a test user
            user = User.query.first()
            if not user:
                print("❌ No users found")
                return
            
            print(f"Testing with user: {user.name}")
            
            # Get wishlist count via API logic
            wishlist = Wishlist.query.filter_by(user_id=user.id).first()
            if not wishlist:
                count = 0
            else:
                count = wishlist.items.count()
            
            print(f"API count: {count}")
            
            # Get actual items
            if wishlist:
                items = wishlist.items.all()
                print(f"Actual items: {len(items)}")
                
                for item in items:
                    product = Product.query.get(item.product_id)
                    if product:
                        print(f"  - {product.name} (ID: {product.id})")
                    else:
                        print(f"  - Invalid product ID: {item.product_id}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔧 Wishlist Count Fix Tool")
    print("=" * 60)
    
    # First diagnose the issue
    diagnose_wishlist_issue()
    
    # Ask user if they want to fix
    print("\n" + "=" * 60)
    response = input("Do you want to fix the wishlist issues? (y/n): ").lower().strip()
    
    if response == 'y':
        fix_wishlist_issues()
    else:
        print("Skipping fixes.")
    
    # Test the API
    test_wishlist_count_api()
    
    print("\n🎉 Wishlist diagnosis completed!") 