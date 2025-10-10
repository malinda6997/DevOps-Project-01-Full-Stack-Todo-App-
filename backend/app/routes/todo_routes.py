from flask import Blueprint, request, jsonify
from app.models.todo import Todo
import logging

logger = logging.getLogger(__name__)
todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    try:
        todos = Todo.find_all()
        todos_dict = [todo.to_dict() for todo in todos]
        return jsonify({"todos": todos_dict, "count": len(todos_dict)})
    except Exception as e:
        logger.error(f"Error fetching todos: {e}")
        return jsonify({"error": "Failed to fetch todos"}), 500

@todo_bp.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({"error": "Title is required"}), 400
        
        if not data['title'].strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        
        todo = Todo(
            title=data['title'].strip(),
            description=data.get('description', '').strip(),
            completed=data.get('completed', False)
        )
        
        saved_todo = todo.save()
        return jsonify({
            "todo": saved_todo.to_dict(), 
            "message": "Todo created successfully"
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        return jsonify({"error": "Failed to create todo"}), 500

@todo_bp.route('/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    try:
        todo = Todo.find_by_id(todo_id)
        
        if not todo:
            return jsonify({"error": "Todo not found"}), 404
        
        return jsonify({"todo": todo.to_dict()})
        
    except Exception as e:
        logger.error(f"Error fetching todo {todo_id}: {e}")
        return jsonify({"error": "Failed to fetch todo"}), 500

@todo_bp.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    try:
        todo = Todo.find_by_id(todo_id)
        
        if not todo:
            return jsonify({"error": "Todo not found"}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Update fields if provided
        update_fields = {}
        if 'title' in data:
            if not data['title'].strip():
                return jsonify({"error": "Title cannot be empty"}), 400
            update_fields['title'] = data['title'].strip()
        
        if 'description' in data:
            update_fields['description'] = data['description'].strip()
        
        if 'completed' in data:
            update_fields['completed'] = bool(data['completed'])
        
        if update_fields:
            updated_todo = todo.update(**update_fields)
            return jsonify({
                "todo": updated_todo.to_dict(), 
                "message": "Todo updated successfully"
            })
        else:
            return jsonify({"error": "No valid fields to update"}), 400
            
    except Exception as e:
        logger.error(f"Error updating todo {todo_id}: {e}")
        return jsonify({"error": "Failed to update todo"}), 500

@todo_bp.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    try:
        deleted = Todo.delete_by_id(todo_id)
        
        if not deleted:
            return jsonify({"error": "Todo not found"}), 404
        
        return jsonify({"message": "Todo deleted successfully"})
        
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id}: {e}")
        return jsonify({"error": "Failed to delete todo"}), 500

@todo_bp.route('/todos/<todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    try:
        todo = Todo.find_by_id(todo_id)
        
        if not todo:
            return jsonify({"error": "Todo not found"}), 404
        
        updated_todo = todo.toggle_completion()
        
        return jsonify({
            "todo": updated_todo.to_dict(), 
            "message": "Todo status toggled successfully"
        })
        
    except Exception as e:
        logger.error(f"Error toggling todo {todo_id}: {e}")
        return jsonify({"error": "Failed to toggle todo status"}), 500

@todo_bp.route('/todos/search', methods=['GET'])
def search_todos():
    """Search todos by title or description"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({"error": "Search query is required"}), 400
        
        # For now, get all todos and filter in Python
        # In production, you might want to use MongoDB text search
        all_todos = Todo.find_all()
        
        matching_todos = [
            todo for todo in all_todos 
            if query.lower() in todo.title.lower() or query.lower() in todo.description.lower()
        ]
        
        todos_dict = [todo.to_dict() for todo in matching_todos]
        
        return jsonify({
            "todos": todos_dict, 
            "count": len(todos_dict),
            "query": query
        })
        
    except Exception as e:
        logger.error(f"Error searching todos: {e}")
        return jsonify({"error": "Failed to search todos"}), 500