from app import create_app
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create the Flask app instance
app = create_app(os.getenv('FLASK_CONFIG') or 'heroku')

def ensure_database_seeded():
    """Ensure database has default products and services"""
    try:
        from auto_startup_seed import check_and_seed_database
        print("🔍 Ensuring database has default products and services...")
        check_and_seed_database()
    except Exception as e:
        print(f"⚠️  Warning: Could not check database seeding: {e}")
        print("The application will start, but you may need to manually seed the database")

if __name__ == '__main__':
    # Ensure database is seeded before starting
    ensure_database_seeded()
    app.run() 