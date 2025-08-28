#!/usr/bin/env python3
"""
Fix admin authentication setup issues
"""
from app import create_app, db
from app.models import AdminUser, AdminRole, SystemSettings
import bcrypt

def check_admin_setup():
    """Check admin authentication setup"""
    
    print("🔍 Checking Admin Authentication Setup")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Check if admin roles exist
            admin_roles = AdminRole.query.all()
            print(f"📊 Admin roles found: {len(admin_roles)}")
            
            if not admin_roles:
                print("❌ No admin roles found - creating default role...")
                create_default_admin_role()
                admin_roles = AdminRole.query.all()
            
            # Check if admin users exist
            admin_users = AdminUser.query.all()
            print(f"👥 Admin users found: {len(admin_users)}")
            
            if not admin_users:
                print("❌ No admin users found - creating default admin...")
                create_default_admin_user(admin_roles[0])
                admin_users = AdminUser.query.all()
            
            # Display admin users
            for admin in admin_users:
                print(f"\n👤 Admin User: {admin.username}")
                print(f"   Email: {admin.email}")
                print(f"   Active: {admin.is_active}")
                print(f"   Super Admin: {admin.is_super_admin}")
                print(f"   Role: {admin.role.name if admin.role else 'No role'}")
                print(f"   Email Verified: {admin.email_verified}")
                
                if admin.role and admin.role.permissions:
                    print(f"   Permissions: {len(admin.role.permissions)}")
                else:
                    print(f"   ⚠️  No permissions assigned")
            
            # Check essential system settings
            print(f"\n⚙️  Checking system settings...")
            essential_settings = [
                'site_name', 'site_description', 'contact_email', 'contact_phone',
                'commission_rate', 'min_withdrawal_amount', 'max_withdrawal_amount'
            ]
            
            for setting_key in essential_settings:
                setting = SystemSettings.query.filter_by(key=setting_key).first()
                if setting:
                    print(f"   ✅ {setting_key}: {setting.value}")
                else:
                    print(f"   ❌ {setting_key}: Missing")
            
            print(f"\n✅ Admin setup check completed!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

def create_default_admin_role():
    """Create default admin role"""
    
    print("🔧 Creating default admin role...")
    
    default_role = AdminRole(
        name='Super Admin',
        description='Full system access with all permissions',
        permissions=[
            'view_dashboard', 'view_settings', 'update_settings', 'create_settings',
            'view_admin_users', 'create_admin_users', 'update_admin_users', 'delete_admin_users',
            'view_activity_logs', 'view_orders', 'update_orders', 'delete_orders',
            'view_products', 'create_products', 'update_products', 'delete_products',
            'view_users', 'update_users', 'delete_users', 'view_reports',
            'view_analytics', 'view_system_monitor', 'manage_cyber_services'
        ],
        is_active=True
    )
    
    db.session.add(default_role)
    db.session.commit()
    print("✅ Default admin role created")

def create_default_admin_user(role):
    """Create default admin user"""
    
    print("🔧 Creating default admin user...")
    
    # Check if admin user already exists
    existing_admin = AdminUser.query.filter_by(email='admin@kibtech.coke').first()
    if existing_admin:
        print("⚠️  Admin user already exists, updating...")
        existing_admin.is_active = True
        existing_admin.role_id = role.id
        existing_admin.is_super_admin = True
        existing_admin.email_verified = True
        db.session.commit()
        print("✅ Admin user updated")
        return
    
    # Create new admin user
    default_admin = AdminUser(
        username='admin',
        email='admin@kibtech.coke',
        first_name='Admin',
        last_name='User',
        phone='+254700000000',
        role_id=role.id,
        is_active=True,
        is_super_admin=True,
        email_verified=True
    )
    
    # Set password
    password = 'admin123'
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    default_admin.password_hash = password_hash.decode('utf-8')
    
    db.session.add(default_admin)
    db.session.commit()
    
    print("✅ Default admin user created")
    print(f"   Username: admin@kibtech.coke")
    print(f"   Password: admin123")
    print(f"   ⚠️  Please change the password after first login!")

def create_essential_settings():
    """Create essential system settings"""
    
    print("🔧 Creating essential system settings...")
    
    essential_settings = [
        ('site_name', 'Kibtech Store', 'general'),
        ('site_description', 'Your trusted online store', 'general'),
        ('contact_email', 'support@kibtech.coke', 'general'),
        ('contact_phone', '+254700000000', 'general'),
        ('commission_rate', '5.0', 'commission'),
        ('min_withdrawal_amount', '100.0', 'withdrawal'),
        ('max_withdrawal_amount', '50000.0', 'withdrawal'),
        ('mpesa_consumer_key', '', 'payment'),
        ('mpesa_consumer_secret', '', 'payment'),
        ('mpesa_passkey', '', 'payment'),
        ('mpesa_environment', 'sandbox', 'payment')
    ]
    
    for key, value, category in essential_settings:
        existing_setting = SystemSettings.query.filter_by(key=key).first()
        if not existing_setting:
            setting = SystemSettings(
                key=key,
                value=value,
                description=f'System setting for {key}',
                category=category,
                is_public=False
            )
            db.session.add(setting)
            print(f"   ✅ Created: {key}")
        else:
            print(f"   ⚠️  Already exists: {key}")
    
    db.session.commit()
    print("✅ Essential settings created")

def test_admin_auth():
    """Test admin authentication"""
    
    print("\n🧪 Testing Admin Authentication")
    print("=" * 50)
    
    app = create_app()
    with app.app_context():
        try:
            # Get admin user
            admin_user = AdminUser.query.filter_by(email='admin@kibtech.coke').first()
            if not admin_user:
                print("❌ Admin user not found")
                return
            
            print(f"Testing with admin: {admin_user.username}")
            
            # Test password
            test_password = 'admin123'
            if admin_user.check_password(test_password):
                print("✅ Password authentication works")
            else:
                print("❌ Password authentication failed")
            
            # Test permissions
            if admin_user.role and admin_user.role.permissions:
                print(f"✅ Has {len(admin_user.role.permissions)} permissions")
            else:
                print("❌ No permissions assigned")
            
            # Test super admin status
            if admin_user.is_super_admin:
                print("✅ Super admin privileges active")
            else:
                print("❌ Not a super admin")
            
            # Test active status
            if admin_user.is_active:
                print("✅ Account is active")
            else:
                print("❌ Account is inactive")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔧 Admin Setup Fix Tool")
    print("=" * 60)
    
    # Check current setup
    check_admin_setup()
    
    # Create essential settings
    print("\n" + "=" * 60)
    response = input("Do you want to create essential system settings? (y/n): ").lower().strip()
    
    if response == 'y':
        create_essential_settings()
    
    # Test authentication
    test_admin_auth()
    
    print("\n🎉 Admin setup completed!")
    print("\n📝 Next Steps:")
    print("1. Try logging into admin panel with admin@kibtech.coke / admin123")
    print("2. Change the default password immediately")
    print("3. Configure M-Pesa settings in admin panel") 