from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from extensions import mongo, jwt, mail
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # Enable CORS
    CORS(
        app,
        resources={r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "https://todo-fullstack-application-enht.onrender.com"
            ]
        }},
        supports_credentials=True
    )

    # ✅ Relax/remove COOP header so Google Sign-In postMessage works
    @app.after_request
    def adjust_security_headers(response):
        # Option 1: remove COOP completely
        response.headers.pop("Cross-Origin-Opener-Policy", None)
        response.headers.pop("Cross-Origin-Embedder-Policy", None)
        
        # Option 2: instead of removing, relax it
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        return response

    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(todo_bp)

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

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
