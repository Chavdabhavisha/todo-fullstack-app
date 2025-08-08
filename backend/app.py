from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configuration from environment
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register Blueprints
    from routes.todos import todos_bp
    from routes.auth import auth_bp
    app.register_blueprint(todos_bp, url_prefix="/api/todos")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app

# Render requires app:app (app object must be defined at root level)
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
