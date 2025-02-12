from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from database import init_db
from routes.auth import auth_bp
from routes.stocks import stocks_bp
from utils.websocket import init_websocket

# Load environment variables
load_dotenv()
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import init_db
from routes.auth import auth_bp
from routes.stocks import stocks_bp
from utils.websocket import init_websocket

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Configure CORS
CORS(app)

# Initialize Database
init_db()


# Add a root route
@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "Welcome to the Stocks Application API"
    }), 200


# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/router/auth")
app.register_blueprint(stocks_bp, url_prefix="/routes/stocks")

# Initialize WebSocket
init_websocket(app)

if __name__ == "__main__":
    app.run(debug=True)
# Initialize Flask App
app = Flask(__name__)

# Configure CORS
CORS(app)

# Initialize Database
init_db()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/router/auth")
app.register_blueprint(stocks_bp, url_prefix="/routes/stocks")

# Initialize WebSocket
init_websocket(app)

if __name__ == "__main__":
    app.run(debug=True)