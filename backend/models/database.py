"""
Simple Database Connection for Todo App
"""
from pymongo import MongoClient
from flask import current_app

# Global database connection
db = None
collection = None

def init_db(app):
    """Initialize MongoDB connection"""
    global db, collection
    
    with app.app_context():
        try:
            # Connect to MongoDB
            client = MongoClient(app.config['MONGO_URI'])
            
            # Test connection
            client.admin.command('ping')
            print("✅ Connected to MongoDB successfully!")
            
            # Get database and collection
            db = client[app.config['DATABASE_NAME']]
            collection = db[app.config['COLLECTION_NAME']]
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise e

def get_collection():
    """Get the todos collection"""
    return collection