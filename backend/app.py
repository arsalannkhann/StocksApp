from flask import Flask, jsonify
from flask_cors import CORS
import logging
from dotenv import load_dotenv

from database import init_db, close_db
from routes.auth import auth_bp
from routes.stocks import stocks_bp

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_app():
    app = Flask(__name__)

    try:
        # Initialize Database on app creation
        init_db()
        logging.info("Database initialized successfully")

        # Configure CORS
        CORS(app, supports_credentials=True)
        logging.info("CORS enabled")

        # Register Blueprints
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(stocks_bp, url_prefix="/stocks")

        # Teardown connections on app context end
        @app.teardown_appcontext
        def shutdown_database(exception=None):
            close_db()
            logging.info("Database connection closed")

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