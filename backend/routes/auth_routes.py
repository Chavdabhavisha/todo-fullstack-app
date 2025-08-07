from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
import datetime
import os
from extensions import mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    # Get credential from request
    credential = request.json.get("credential")
    if not credential:
        return jsonify({"error": "Missing credential"}), 400

    try:
        # Verify the Google ID token
        idinfo = id_token.verify_oauth2_token(
            credential,
            grequests.Request(),
            os.getenv("GOOGLE_CLIENT_ID")  # Loaded from .env
        )

        # Extract the user's email
        email = idinfo.get("email")
        if not email:
            return jsonify({"error": "Email not found in token"}), 400

        # Check if user exists, if not insert new user
        user = mongo.db.users.find_one({"email": email})
        if not user:
            mongo.db.users.insert_one({"email": email})

        # Generate JWT token valid for 1 day
        access_token = create_access_token(
            identity=email,
            expires_delta=datetime.timedelta(days=1)
        )

        return jsonify({"token": access_token}), 200

    except ValueError as ve:
        return jsonify({"error": "Invalid token", "details": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
