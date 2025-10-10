"""
Simple Flask Todo App - Main Entry Point
"""
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Configuration
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    app.config['DATABASE_NAME'] = os.getenv('DATABASE_NAME', 'todoapp')
    app.config['COLLECTION_NAME'] = os.getenv('COLLECTION_NAME', 'todos')
    
    # Initialize database
    from models.database import init_db
    init_db(app)
    
    # Register routes
    from routes.todo_routes import todo_bp
    app.register_blueprint(todo_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Flask backend is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting Flask Todo App...")
    print("Visit: http://127.0.0.1:5000/api/todos")
    app.run(debug=True, host='0.0.0.0', port=5000)