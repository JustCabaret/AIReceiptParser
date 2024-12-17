from flask import Flask
from flask_cors import CORS
from app.routes import blueprint

def create_app():
    app = Flask(__name__)
    
    # Ativa o CORS para todas as rotas
    CORS(app, resources={r"/*": {"origins": "*"}})  # Permite acesso de qualquer origem

    app.register_blueprint(blueprint)
    return app
