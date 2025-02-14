from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import logging

from database import init_db, close_db
from routes.auth import auth_bp
from routes.stocks import stocks_bp
from utils.websocket import init_websocket
from utils.auth_utils import login_required

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS

init_websocket(app)  # Initialize WebSocket
init_db()  # Initialize Database

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(stocks_bp, url_prefix="/api/stocks")

@app.route('/')
def index():
    return jsonify({"status": "ok", "message": "Stocks Application API"})

@app.teardown_appcontext
def close_connection(exception):
    close_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)