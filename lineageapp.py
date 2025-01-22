from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Set the database URI to point to lineage.db in the parent folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "../lineage.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure secret key
    
    # Initialize the database with the app
    db.init_app(app)
    
    # Import and register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app