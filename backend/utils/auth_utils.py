# utils/auth_utils.py
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import firebase_admin
from firebase_admin import auth
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def generate_token(user_id: str) -> str:
    secret_key = os.getenv("SECRET_KEY")
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401

        try:
            id_token = auth_header.split('Bearer ')[1]
            decoded_token = auth.verify_id_token(id_token)
            request.decoded_token = decoded_token
        except ValueError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)
    return decorated_function