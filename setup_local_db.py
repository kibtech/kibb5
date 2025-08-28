#!/usr/bin/env python3
"""
Setup local PostgreSQL database for development
"""

import os
import psycopg2
from sqlalchemy import create_engine, text

def setup_local_database():
    """Setup local PostgreSQL database"""
    print("🔧 Setting up Local Database")
    print("=" * 40)
    
    # Local database configuration
    db_config = {
        'host': 'localhost',
        'database': 'kibtech',
        'user': 'postgres',
        'password': 'password',
        'port': '5432'
    }
    
    try:
        # Connect to PostgreSQL server (without specifying database)
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port']
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_config['database'],))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database '{db_config['database']}'...")
            cur.execute(f"CREATE DATABASE {db_config['database']}")
            print("✅ Database created successfully")
        else:
            print(f"✅ Database '{db_config['database']}' already exists")
        
        cur.close()
        conn.close()
        
        # Now connect to the specific database and create tables
        print("Connecting to database and creating tables...")
        engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")
        
        with engine.connect() as conn:
            # Create tables using SQLAlchemy
            from app import create_app, db
            app = create_app()
            
            with app.app_context():
                # Create all tables
                db.create_all()
                print("✅ All tables created successfully")
                
                # Add email_verified column if it doesn't exist
                try:
                    conn.execute(text("SELECT email_verified FROM users LIMIT 1"))
                    print("✅ email_verified column already exists")
                except Exception as e:
                    if "column users.email_verified does not exist" in str(e) or "column \"email_verified\" does not exist" in str(e):
                        print("Adding email_verified column...")
                        conn.execute(text("ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE"))
                        conn.commit()
                        print("✅ email_verified column added successfully")
                    else:
                        raise e
        
        print("\n🎉 Local database setup completed successfully!")
        print("You can now use the local database by setting USE_LOCAL_DB=true")
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting local database setup...")
    setup_local_database()
    print("Setup completed.") 