"""
Simple Todo Model
"""
from datetime import datetime
from bson import ObjectId
from models.database import get_collection

class Todo:
    def __init__(self, title, description="", completed=False, _id=None):
        self._id = _id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self._id) if self._id else None,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def save(self):
        """Save todo to database"""
        collection = get_collection()
        
        todo_data = {
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if self._id:
            # Update existing
            collection.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': todo_data}
            )
        else:
            # Create new
            result = collection.insert_one(todo_data)
            self._id = result.inserted_id
        
        return self
    
    @classmethod
    def find_all(cls):
        """Get all todos"""
        collection = get_collection()
        todos = collection.find().sort('created_at', -1)
        
        return [cls._from_mongo(todo) for todo in todos]
    
    @classmethod
    def find_by_id(cls, todo_id):
        """Find todo by ID"""
        collection = get_collection()
        todo = collection.find_one({'_id': ObjectId(todo_id)})
        
        if todo:
            return cls._from_mongo(todo)
        return None
    
    @classmethod
    def delete_by_id(cls, todo_id):
        """Delete todo by ID"""
        collection = get_collection()
        result = collection.delete_one({'_id': ObjectId(todo_id)})
        
        return result.deleted_count > 0
    
    @classmethod
    def _from_mongo(cls, data):
        """Create Todo from MongoDB document"""
        return cls(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            _id=data['_id']
        )