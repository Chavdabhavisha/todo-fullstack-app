from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from extensions import mongo, jwt, mail  # ✅ also import mail
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp

# 🔄 Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # 🔐 Configuration
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # ✅ Mail Configuration from .env
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    # 🔗 Enable CORS for frontend (update origin later for production)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    # 🧩 Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)  # ✅ Initialize Flask-Mail

    # 📦 Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(todo_bp)  # Already has /api/todos prefix in todo_bp

    return app

# 🚀 Run server for production (Render)
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
