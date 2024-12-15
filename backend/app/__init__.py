from flask import Flask
from app.routes import blueprint

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Register the blueprint for API routes
    app.register_blueprint(blueprint)

    return app
