from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
from flask import current_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """MongoDB database connection manager"""
    
    def __init__(self):
        self.client = None
        self.db = None
        
    def initialize_db(self, app):
        """Initialize MongoDB connection with Flask app"""
        try:
            # Get MongoDB URI from config
            mongo_uri = app.config['MONGO_URI']
            database_name = app.config['DATABASE_NAME']
            
            # Create MongoDB client
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,         # 10 second timeout
                socketTimeoutMS=20000           # 20 second timeout
            )
            
            # Test the connection
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
            # Get the database
            self.db = self.client[database_name]
            
            # Create indexes for better performance
            self._create_indexes()
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise Exception(f"Database connection failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during database initialization: {e}")
            raise
    
    def _create_indexes(self):
        """Create database indexes for optimization"""
        try:
            collection_name = current_app.config['COLLECTION_NAME']
            collection = self.db[collection_name]
            
            # Create index on 'created_at' for efficient sorting
            collection.create_index([("created_at", -1)])
            
            # Create text index for searching todos
            collection.create_index([("title", "text"), ("description", "text")])
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Failed to create indexes: {e}")
    
    def get_collection(self, collection_name=None):
        """Get a MongoDB collection"""
        if not self.db:
            raise Exception("Database not initialized")
        
        if not collection_name:
            collection_name = current_app.config['COLLECTION_NAME']
        
        return self.db[collection_name]
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Create a global database instance
db = Database()