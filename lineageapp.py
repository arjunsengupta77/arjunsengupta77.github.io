from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from lineage.glossary.routes import glossary_bp
    from lineage.visualization.routes import visualization_bp

    app.register_blueprint(glossary_bp, url_prefix="/glossary")
    app.register_blueprint(visualization_bp, url_prefix="/visualization")

    return app)