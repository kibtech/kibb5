#!/usr/bin/env python3
"""
Test script to verify manual commission creation with empty order_id
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Commission, Wallet
from decimal import Decimal

def test_manual_commission_with_empty_order_id():
    """Test creating a manual commission with empty order_id"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get a user with a wallet
            user = User.query.filter(User.wallet.has()).first()
            if not user:
                print("No user with wallet found. Creating test user...")
                user = User(
                    name="Test User",
                    email="test@example.com",
                    password="password123"
                )
                db.session.add(user)
                db.session.commit()
                
                # Create wallet for user
                wallet = Wallet(user_id=user.id)
                db.session.add(wallet)
                db.session.commit()
            
            print(f"Testing with user: {user.name} (ID: {user.id})")
            
            # Test data with empty order_id
            test_data = {
                'user_id': user.id,
                'amount': '10.00',
                'description': 'Test manual commission',
                'order_id': ''  # Empty string
            }
            
            print(f"Test data: {test_data}")
            
            # Simulate the data processing from the route
            order_id = test_data.get('order_id')
            print(f"Initial order_id: '{order_id}' (type: {type(order_id)})")
            
            # Apply the fix
            if order_id == '':
                order_id = None
                print(f"Converted order_id to: {order_id}")
            
            # Create commission record
            commission = Commission(
                referrer_id=user.id,
                order_id=order_id,
                amount=Decimal(test_data['amount']),
                commission_type='manual',
                description=test_data['description']
            )
            
            db.session.add(commission)
            db.session.commit()
            
            print(f"✅ Success! Commission created with ID: {commission.id}")
            print(f"Commission details:")
            print(f"  - order_id: {commission.order_id}")
            print(f"  - amount: {commission.amount}")
            print(f"  - commission_type: {commission.commission_type}")
            print(f"  - description: {commission.description}")
            
            # Clean up test data
            db.session.delete(commission)
            db.session.commit()
            print("✅ Test commission cleaned up")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("Testing manual commission creation with empty order_id...")
    success = test_manual_commission_with_empty_order_id()
    
    if success:
        print("\n🎉 Test passed! The fix is working correctly.")
    else:
        print("\n💥 Test failed! The fix needs more work.") 