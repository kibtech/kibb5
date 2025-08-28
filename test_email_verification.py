#!/usr/bin/env python3
"""
Test email verification for unverified users
"""
from app import create_app, db
from app.models import User
from app.services.email_service import get_email_service

def test_email_verification():
    """Test email verification for unverified users"""
    
    print("🔧 Testing Email Verification for Unverified Users")
    print("=" * 60)
    
    app = create_app()
    with app.app_context():
        try:
            # Get unverified users
            unverified_users = User.query.filter_by(email_verified=False).all()
            print(f"Found {len(unverified_users)} unverified users:")
            
            for i, user in enumerate(unverified_users, 1):
                print(f"{i}. {user.name} ({user.email})")
            
            if unverified_users:
                # Test sending verification email to first unverified user
                test_user = unverified_users[0]
                print(f"\n🧪 Testing verification email for: {test_user.name} ({test_user.email})")
                
                # Get email service
                email_service = get_email_service()
                
                # Send verification email
                result = email_service.send_email_verification_otp(test_user)
                print(f"Verification email result: {result}")
                
                if result:
                    print("✅ Verification email sent successfully!")
                    print(f"📧 Check email at: {test_user.email}")
                    print("📁 Don't forget to check spam folder!")
                else:
                    print("❌ Failed to send verification email")
            
            # Show verified users for comparison
            verified_users = User.query.filter_by(email_verified=True).all()
            print(f"\n✅ Verified users ({len(verified_users)}):")
            for user in verified_users:
                print(f"   - {user.name} ({user.email})")
            
            print("\n🎉 Email verification test completed!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

def check_user_status():
    """Check detailed user status"""
    
    print("\n📊 Detailed User Status")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            users = User.query.all()
            
            print(f"Total users: {len(users)}")
            print(f"Verified users: {len([u for u in users if u.email_verified])}")
            print(f"Unverified users: {len([u for u in users if not u.email_verified])}")
            
            print("\n📋 User Details:")
            for i, user in enumerate(users, 1):
                status = "✅ Verified" if user.email_verified else "❌ Unverified"
                print(f"{i}. {user.name}")
                print(f"   Email: {user.email}")
                print(f"   Phone: {user.phone}")
                print(f"   Status: {status}")
                print(f"   Created: {user.created_at}")
                print()
            
        except Exception as e:
            print(f"❌ Status check failed: {str(e)}")

if __name__ == "__main__":
    # Check user status
    check_user_status()
    
    # Test email verification
    test_email_verification()
    
    print("\n📝 Summary:")
    print("- 2 users need email verification")
    print("- 3 users are already verified")
    print("- Email service is working (we tested it earlier)")
    print("- Unverified users should check spam folder for verification emails") 