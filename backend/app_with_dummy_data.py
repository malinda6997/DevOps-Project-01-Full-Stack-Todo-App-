from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Temporary in-memory storage with dummy data for testing
todos = [
    {
        "id": "1",
        "title": "Learn Flask API Development",
        "description": "Build a complete REST API with Flask and MongoDB integration",
        "completed": False,
        "created_at": "2025-10-10T09:00:00.000000",
        "updated_at": "2025-10-10T09:00:00.000000"
    },
    {
        "id": "2", 
        "title": "Setup MongoDB Database",
        "description": "Configure MongoDB Atlas or local MongoDB for the todo application",
        "completed": True,
        "created_at": "2025-10-10T10:00:00.000000",
        "updated_at": "2025-10-10T10:30:00.000000"
    },
    {
        "id": "3",
        "title": "Test API with Postman",
        "description": "Create comprehensive test cases for all API endpoints using Postman",
        "completed": False,
        "created_at": "2025-10-10T11:00:00.000000",
        "updated_at": "2025-10-10T11:00:00.000000"
    }
]

next_id = 4

@app.route('/')
def home():
    return {"message": "Todo App Backend API with Dummy Data", "status": "running", "database": "In-Memory (Testing)"}

@app.route('/health')
def health_check():
    return {"status": "healthy", "service": "todo-backend", "database": "In-Memory", "todos_count": len(todos)}

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify({"todos": todos, "count": len(todos)})

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    global next_id
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    if not data['title'].strip():
        return jsonify({"error": "Title cannot be empty"}), 400
    
    new_todo = {
        "id": str(next_id),
        "title": data['title'].strip(),
        "description": data.get('description', '').strip(),
        "completed": data.get('completed', False),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    todos.append(new_todo)
    next_id += 1
    
    return jsonify({"todo": new_todo, "message": "Todo created successfully"}), 201

@app.route('/api/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    return jsonify({"todo": todo})

@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'title' in data:
        if not data['title'].strip():
            return jsonify({"error": "Title cannot be empty"}), 400
        todo['title'] = data['title'].strip()
    
    if 'description' in data:
        todo['description'] = data['description'].strip()
    
    if 'completed' in data:
        todo['completed'] = bool(data['completed'])
    
    todo['updated_at'] = datetime.now().isoformat()
    
    return jsonify({"todo": todo, "message": "Todo updated successfully"})

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    todos = [t for t in todos if t['id'] != todo_id]
    
    return jsonify({"message": "Todo deleted successfully"})

@app.route('/api/todos/<todo_id>/toggle', methods=['PATCH'])
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    todo['completed'] = not todo['completed']
    todo['updated_at'] = datetime.now().isoformat()
    
    return jsonify({"todo": todo, "message": "Todo status toggled successfully"})

@app.route('/api/todos/search', methods=['GET'])
def search_todos():
    """Search todos by title or description"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({"error": "Search query is required"}), 400
    
    matching_todos = [
        todo for todo in todos 
        if query.lower() in todo['title'].lower() or query.lower() in todo['description'].lower()
    ]
    
    return jsonify({
        "todos": matching_todos, 
        "count": len(matching_todos),
        "query": query
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)