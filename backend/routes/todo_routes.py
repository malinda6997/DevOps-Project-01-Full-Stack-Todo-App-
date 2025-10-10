"""
Simple Todo Routes
"""
from flask import Blueprint
from controllers.todo_controller import TodoController

# Create blueprint
todo_bp = Blueprint('todos', __name__)

# Routes
@todo_bp.route('/todos', methods=['GET'])
def get_todos():
    """GET /api/todos - Get all todos"""
    return TodoController.get_all_todos()

@todo_bp.route('/todos', methods=['POST'])
def create_todo():
    """POST /api/todos - Create a new todo"""
    return TodoController.create_todo()

@todo_bp.route('/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """GET /api/todos/:id - Get a specific todo"""
    return TodoController.get_todo(todo_id)

@todo_bp.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """PUT /api/todos/:id - Update a todo"""
    return TodoController.update_todo(todo_id)

@todo_bp.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """DELETE /api/todos/:id - Delete a todo"""
    return TodoController.delete_todo(todo_id)

@todo_bp.route('/health', methods=['GET'])
def health_check():
    """GET /api/health - Health check endpoint"""
    from flask import jsonify
    return jsonify({'status': 'OK', 'message': 'Todo API is running!'})