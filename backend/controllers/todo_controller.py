"""
Simple Todo Controller
"""
from flask import jsonify, request
from models.todo import Todo

class TodoController:
    
    @staticmethod
    def get_all_todos():
        """Get all todos"""
        try:
            todos = Todo.find_all()
            return jsonify({
                'todos': [todo.to_dict() for todo in todos],
                'count': len(todos)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def create_todo():
        """Create a new todo"""
        try:
            data = request.get_json()
            
            if not data or 'title' not in data:
                return jsonify({'error': 'Title is required'}), 400
            
            todo = Todo(
                title=data['title'],
                description=data.get('description', ''),
                completed=data.get('completed', False)
            )
            
            todo.save()
            
            return jsonify({
                'todo': todo.to_dict(),
                'message': 'Todo created successfully'
            }), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def get_todo(todo_id):
        """Get a specific todo"""
        try:
            todo = Todo.find_by_id(todo_id)
            
            if not todo:
                return jsonify({'error': 'Todo not found'}), 404
            
            return jsonify({'todo': todo.to_dict()})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def update_todo(todo_id):
        """Update a todo"""
        try:
            todo = Todo.find_by_id(todo_id)
            
            if not todo:
                return jsonify({'error': 'Todo not found'}), 404
            
            data = request.get_json()
            
            if 'title' in data:
                todo.title = data['title']
            if 'description' in data:
                todo.description = data['description']
            if 'completed' in data:
                todo.completed = data['completed']
            
            todo.save()
            
            return jsonify({
                'todo': todo.to_dict(),
                'message': 'Todo updated successfully'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def delete_todo(todo_id):
        """Delete a todo"""
        try:
            if Todo.delete_by_id(todo_id):
                return jsonify({'message': 'Todo deleted successfully'})
            else:
                return jsonify({'error': 'Todo not found'}), 404
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500