from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging

from database import init_db
from routes.auth import auth_bp
from routes.stocks import stocks_bp
from utils.websocket import init_websocket

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    try:
        # Configure CORS
        CORS(app, supports_credentials=True)
        logging.info("CORS enabled")

        # Initialize Database
        init_db()
        logging.info("Database initialized successfully")

        # Register Blueprints
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(stocks_bp, url_prefix="/stocks")
        logging.info("Blueprints registered")

        # Initialize WebSocket
        init_websocket(app)
        logging.info("WebSocket initialized")

    except Exception as e:
        logging.error(f"Error during app initialization: {e}")
        return None

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
    if app:
        app.run(debug=True, host="0.0.0.0", port=5000)
    else:
        logging.error("Failed to start Flask app due to initialization errors")