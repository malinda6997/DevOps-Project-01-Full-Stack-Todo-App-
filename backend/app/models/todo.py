from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.database import db
import logging

logger = logging.getLogger(__name__)

class Todo:
    """Todo model class for MongoDB operations"""
    
    def __init__(self, title, description="", completed=False, _id=None, created_at=None, updated_at=None):
        self._id = _id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert todo object to dictionary"""
        return {
            'id': str(self._id) if self._id else None,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    def save(self):
        """Save todo to MongoDB"""
        try:
            collection = db.get_collection()
            self.updated_at = datetime.utcnow()
            
            todo_data = {
                'title': self.title,
                'description': self.description,
                'completed': self.completed,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
            
            if self._id:
                # Update existing todo
                result = collection.update_one(
                    {'_id': ObjectId(self._id)},
                    {'$set': todo_data}
                )
                if result.matched_count == 0:
                    raise ValueError("Todo not found")
                return self
            else:
                # Create new todo
                result = collection.insert_one(todo_data)
                self._id = result.inserted_id
                return self
                
        except PyMongoError as e:
            logger.error(f"Database error while saving todo: {e}")
            raise Exception(f"Failed to save todo: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while saving todo: {e}")
            raise
    
    @classmethod
    def find_all(cls):
        """Get all todos from MongoDB"""
        try:
            collection = db.get_collection()
            todos = collection.find().sort('created_at', -1)
            return [cls._from_mongo(todo) for todo in todos]
        except PyMongoError as e:
            logger.error(f"Database error while fetching todos: {e}")
            raise Exception(f"Failed to fetch todos: {e}")
    
    @classmethod
    def find_by_id(cls, todo_id):
        """Find todo by ID"""
        try:
            collection = db.get_collection()
            todo = collection.find_one({'_id': ObjectId(todo_id)})
            return cls._from_mongo(todo) if todo else None
        except PyMongoError as e:
            logger.error(f"Database error while finding todo by ID: {e}")
            raise Exception(f"Failed to find todo: {e}")
        except Exception as e:
            logger.error(f"Invalid todo ID format: {e}")
            return None
    
    @classmethod
    def delete_by_id(cls, todo_id):
        """Delete todo by ID"""
        try:
            collection = db.get_collection()
            result = collection.delete_one({'_id': ObjectId(todo_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            logger.error(f"Database error while deleting todo: {e}")
            raise Exception(f"Failed to delete todo: {e}")
        except Exception as e:
            logger.error(f"Invalid todo ID format: {e}")
            return False
    
    def update(self, **kwargs):
        """Update todo attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        return self.save()
    
    def toggle_completion(self):
        """Toggle the completion status"""
        self.completed = not self.completed
        self.updated_at = datetime.utcnow()
        return self.save()
    
    @classmethod
    def _from_mongo(cls, mongo_doc):
        """Create Todo instance from MongoDB document"""
        if not mongo_doc:
            return None
        
        return cls(
            _id=mongo_doc['_id'],
            title=mongo_doc['title'],
            description=mongo_doc.get('description', ''),
            completed=mongo_doc.get('completed', False),
            created_at=mongo_doc.get('created_at'),
            updated_at=mongo_doc.get('updated_at')
        )
    
    def __str__(self):
        return f"Todo(id={self._id}, title='{self.title}', completed={self.completed})"
    
    def __repr__(self):
        return self.__str__()