#!/usr/bin/env python3
"""
Script to fix the admin_users table by adding missing columns
"""
from app import create_app, db
from sqlalchemy import text

def fix_admin_users_table():
    """Add missing columns to admin_users table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if avatar_url column exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'admin_users' AND column_name = 'avatar_url'
            """))
            
            if not result.fetchone():
                print("Adding avatar_url column to admin_users table...")
                db.session.execute(text("""
                    ALTER TABLE admin_users 
                    ADD COLUMN avatar_url VARCHAR(500)
                """))
                db.session.commit()
                print("✅ avatar_url column added successfully!")
            else:
                print("✅ avatar_url column already exists!")
            
            # Check for other potentially missing columns
            missing_columns = []
            
            # List of columns that should exist in admin_users table
            expected_columns = [
                'mfa_enabled', 'mfa_secret', 'backup_codes', 'password_changed_at',
                'failed_login_attempts', 'last_failed_login', 'password_reset_token',
                'password_reset_expires', 'allowed_ip_addresses', 'session_timeout',
                'force_password_change', 'email_verified', 'timezone', 'language',
                'theme', 'notifications_enabled'
            ]
            
            for column in expected_columns:
                result = db.session.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'admin_users' AND column_name = '{column}'
                """))
                
                if not result.fetchone():
                    missing_columns.append(column)
            
            if missing_columns:
                print(f"Missing columns: {missing_columns}")
                print("Adding missing columns...")
                
                for column in missing_columns:
                    if column in ['mfa_enabled', 'force_password_change', 'email_verified', 'notifications_enabled']:
                        # Boolean columns
                        db.session.execute(text(f"""
                            ALTER TABLE admin_users 
                            ADD COLUMN {column} BOOLEAN DEFAULT FALSE
                        """))
                    elif column in ['failed_login_attempts', 'session_timeout']:
                        # Integer columns
                        db.session.execute(text(f"""
                            ALTER TABLE admin_users 
                            ADD COLUMN {column} INTEGER DEFAULT 0
                        """))
                    elif column in ['mfa_secret', 'password_reset_token', 'timezone', 'language', 'theme']:
                        # String columns
                        db.session.execute(text(f"""
                            ALTER TABLE admin_users 
                            ADD COLUMN {column} VARCHAR(50)
                        """))
                    elif column in ['backup_codes', 'allowed_ip_addresses']:
                        # JSON columns
                        db.session.execute(text(f"""
                            ALTER TABLE admin_users 
                            ADD COLUMN {column} JSON
                        """))
                    else:
                        # DateTime columns
                        db.session.execute(text(f"""
                            ALTER TABLE admin_users 
                            ADD COLUMN {column} TIMESTAMP
                        """))
                
                db.session.commit()
                print(f"✅ Added {len(missing_columns)} missing columns!")
            else:
                print("✅ All expected columns exist!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    fix_admin_users_table() 