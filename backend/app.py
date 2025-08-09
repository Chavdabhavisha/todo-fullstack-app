from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from extensions import mongo, jwt, mail
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Mail Configuration
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # Enable CORS for frontend running on localhost:3000
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(todo_bp)

    # Root route for health check
    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "Backend is running!",
            "endpoints": {
                "auth": "/api/auth",
                "todos": "/api/todos"
            }
        })

    return app

# Run server
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
