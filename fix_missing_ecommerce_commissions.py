#!/usr/bin/env python3
"""
Fix Missing E-commerce Commissions
Retroactively processes commissions for paid orders that were missing them.
"""
import os
import sys
from decimal import Decimal
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User, Order, Commission, Wallet, SystemSettings

def fix_missing_commissions():
    """Fix missing commissions for existing paid orders"""
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Fixing Missing E-commerce Commissions...")
        print("=" * 50)
        
        # Get commission rate
        commission_setting = db.session.query(SystemSettings).filter_by(key='ecommerce_commission_rate').first()
        commission_rate = float(commission_setting.value) / 100.0 if commission_setting else 0.03  # 3% default
        print(f"📊 Using commission rate: {commission_rate * 100}%")
        
        # Find paid orders from referred users that don't have commissions
        print("\n🔍 Finding paid orders missing commissions...")
        
        # Query for paid orders from referred users
        paid_orders_from_referred = db.session.query(Order).join(User).filter(
            Order.payment_status == 'paid',
            User.referred_by_id.isnot(None)
        ).all()
        
        print(f"✅ Found {len(paid_orders_from_referred)} paid orders from referred users")
        
        # Check which ones are missing commissions
        missing_commissions = []
        for order in paid_orders_from_referred:
            existing_commission = db.session.query(Commission).filter_by(order_id=order.id).first()
            if not existing_commission:
                missing_commissions.append(order)
        
        print(f"❌ {len(missing_commissions)} orders are missing commissions")
        
        if not missing_commissions:
            print("✅ No missing commissions found! All orders already have proper commissions.")
            return
        
        print("\n📦 Orders that need commission processing:")
        print("=" * 45)
        
        total_fixed = 0
        total_commission_amount = Decimal('0')
        
        for order in missing_commissions:
            user = order.user
            referrer = db.session.get(User, user.referred_by_id) if user.referred_by_id else None
            
            print(f"\n📦 Order: {order.order_number}")
            print(f"   User: {user.name} (ID: {user.id})")
            print(f"   Referrer: {referrer.name if referrer else 'Unknown'} (ID: {user.referred_by_id})")
            print(f"   Amount: KSh {order.total_amount}")
            print(f"   Created: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            if not referrer:
                print(f"   ⚠️  Referrer not found, skipping...")
                continue
            
            if not referrer.wallet:
                print(f"   ⚠️  Referrer has no wallet, skipping...")
                continue
            
            # Calculate commission
            commission_amount = Decimal(str(float(order.total_amount) * commission_rate))
            print(f"   💰 Commission to add: KSh {commission_amount}")
            
            # Ask for confirmation before processing
            print(f"   🤔 Process this commission? (y/n): ", end='')
            confirm = input().strip().lower()
            
            if confirm in ['y', 'yes']:
                try:
                    # Create commission record
                    commission = Commission(
                        referrer_id=user.referred_by_id,
                        order_id=order.id,
                        amount=commission_amount,
                        commission_type='order',
                        description=f'Commission from order {order.order_number} (retroactive fix)'
                    )
                    db.session.add(commission)
                    
                    # Update referrer's wallet
                    old_balance = referrer.wallet.commission_balance
                    referrer.wallet.add_commission(commission_amount)
                    new_balance = referrer.wallet.commission_balance
                    
                    db.session.commit()
                    
                    print(f"   ✅ Commission processed successfully!")
                    print(f"      Referrer balance: KSh {old_balance} → KSh {new_balance}")
                    
                    total_fixed += 1
                    total_commission_amount += commission_amount
                    
                    # Send notification email (optional)
                    try:
                        from app.services.email_service import get_email_service
                        import logging
                        email_service = get_email_service()
                        
                        # Prepare order details for email
                        order_details = {
                            'order_number': order.order_number,
                            'total_amount': float(order.total_amount),
                            'created_at': order.created_at.strftime('%B %d, %Y at %I:%M %p')
                        }
                        
                        # Send commission notification
                        email_service.send_commission_notification(
                            to_email=referrer.email,
                            referrer_name=referrer.name,
                            commission_amount=float(commission_amount),
                            order_details=order_details,
                            referred_user_name=user.name
                        )
                        
                        print(f"      📧 Notification email sent to {referrer.email}")
                        
                    except Exception as e:
                        print(f"      ⚠️  Email notification failed: {str(e)}")
                        # Don't fail the commission process if email fails
                    
                except Exception as e:
                    db.session.rollback()
                    print(f"   ❌ Error processing commission: {str(e)}")
            else:
                print(f"   ⏭️  Skipped")
        
        print(f"\n📊 Summary:")
        print("=" * 20)
        print(f"✅ Orders fixed: {total_fixed}")
        print(f"💰 Total commissions processed: KSh {total_commission_amount}")
        
        if total_fixed > 0:
            print(f"\n🎉 Successfully fixed {total_fixed} missing commissions!")
        else:
            print(f"\n💡 No commissions were processed.")

if __name__ == "__main__":
    print("🚀 Fix Missing E-commerce Commissions")
    print("-" * 45)
    
    print("⚠️  WARNING: This will process missing commissions for existing paid orders.")
    print("🤔 Are you sure you want to continue? (y/n): ", end='')
    confirm = input().strip().lower()
    
    if confirm in ['y', 'yes']:
        fix_missing_commissions()
    else:
        print("❌ Operation cancelled.")
    
    print("\n✅ Script completed!")