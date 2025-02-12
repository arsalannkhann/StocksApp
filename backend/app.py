from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import init_db
from routes.auth import auth_bp
from routes.stocks import stocks_bp
from utils.websocket import init_websocket

# Load environment variables
load_dotenv()

def create_app():
    """Factory function to create Flask app"""
    app = Flask(__name__)

    # Configure CORS
    CORS(app)

    # Initialize Database
    init_db()

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(stocks_bp, url_prefix="/stocks")

    # Initialize WebSocket
    init_websocket(app)

    # Root Route
    @app.route('/')
    def index():
        return jsonify({
            "status": "ok",
            "message": "Welcome to the Stocks Application API"
        }), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)# In stock_data.py or wherever the import is happening
