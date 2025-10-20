import os
from app import app, db

print("🔧 Resetting database...")

with app.app_context():
    try:
        # Drop all tables
        db.drop_all()
        print("✅ Tables dropped")
        
        # Create all tables with new schema
        db.create_all()
        print("✅ Tables created")
        
        print("🎉 Database reset successful!")
        print("📁 New database file: tripstar.db")
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")