from flask import Flask
from flask_cors import CORS
from app.routes import blueprint
from dotenv import load_dotenv
from modules.database import init_db

def create_app():
    # Load environment variables from .env file
    load_dotenv()
    
    # Initialize SQLite database file and tables
    init_db()

    app = Flask(__name__)
    
    # Ativa o CORS para todas as rotas
    CORS(app, resources={r"/*": {"origins": "*"}})  # Permite acesso de qualquer origem

    app.register_blueprint(blueprint)
    return app
