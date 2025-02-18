# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from backend.utils.auth_utils import generate_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password":
        token = generate_token(username)
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401