import jwt
import datetime
from flask import request, jsonify
from backend.config import config

SECRET_KEY = config.SECRET_KEY

def generate_token(user_id):
    """Generates a JWT token with user_id and expiration time."""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    """Verifies and decodes a JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def authenticate():
    """Extracts and verifies token from request headers."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed token"}), 401

    token = auth_header.split("Bearer ")[1]
    
    # 🔹 Ensure verify_token() is actually called
    decoded_token = verify_token(token)
    
    if "error" in decoded_token:
        return jsonify(decoded_token), 403

    return decoded_token  # Return user details if successful