from flask import Flask
from flask_cors import CORS
from app.database import db

def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)
    
    # Enable CORS for all domains
    CORS(app)
    
    # Load configuration
    app.config.from_object('config.Config')
    
    # Initialize database
    try:
        db.initialize_db(app)
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Application will start but database operations may fail")
    
    # Register blueprints
    from app.routes.todo_routes import todo_bp
    app.register_blueprint(todo_bp, url_prefix='/api')
    
    @app.route('/')
    def home():
        return {"message": "Todo App Backend API", "status": "running", "database": "MongoDB"}
    
    @app.route('/health')
    def health_check():
        return {"status": "healthy", "service": "todo-backend", "database": "MongoDB"}
    
    return app