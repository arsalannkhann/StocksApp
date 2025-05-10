import os
import json
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import redis
import pymongo
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import logging
import sys
sys.path.append('/app')

# Import custom modules
from services.database_service import DatabaseService
from services.prediction_service import PredictionService
from services.data_fetcher import DataFetcher

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize services
db_service = DatabaseService()
prediction_service = PredictionService(db_service)
data_fetcher = DataFetcher()

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
PREDICTION_ACCURACY = Gauge('model_prediction_accuracy', 'Model prediction accuracy')
ACTIVE_CONNECTIONS = Gauge('websocket_connections', 'Active WebSocket connections')
PREDICTION_COUNT = Counter('predictions_total', 'Total predictions made', ['ticker'])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    REQUEST_DURATION.observe(duration)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    return response

@app.route('/api/health')
def health_check():
    try:
        db_status = db_service.health_check()
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": db_status,
            "version": "1.0.0"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict_stock():
    try:
        data = request.get_json()
        ticker = data.get('ticker', 'AAPL').upper()

        if not ticker or len(ticker) > 10:
            return jsonify({"error": "Invalid ticker symbol"}), 400

        prediction = prediction_service.get_prediction(ticker)

        if prediction:
            PREDICTION_COUNT.labels(ticker=ticker).inc()
            socketio.emit('prediction_update', {
                'ticker': ticker,
                'prediction': prediction,
                'timestamp': datetime.now().isoformat()
            })
            return jsonify(prediction), 200
        else:
            return jsonify({"error": "Unable to generate prediction"}), 500

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/history/<ticker>')
def get_stock_history(ticker):
    try:
        ticker = ticker.upper()
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 100)), 1000)
        days = int(request.args.get('days', 30))

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        history = db_service.get_stock_history(ticker, start_date, end_date, page, limit)

        return jsonify({
            "ticker": ticker,
            "data": history,
            "page": page,
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid parameters"}), 400
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/sentiment/<ticker>')
def get_sentiment_analysis(ticker):
    try:
        ticker = ticker.upper()
        sentiment_data = db_service.get_sentiment_data(ticker)

        return jsonify({
            "ticker": ticker,
            "sentiment": sentiment_data,
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Sentiment retrieval error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/tickers')
def get_available_tickers():
    try:
        tickers = db_service.get_available_tickers()
        return jsonify({
            "tickers": tickers,
            "count": len(tickers),
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Tickers retrieval error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/metrics')
def metrics():
    from flask import Response
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    ACTIVE_CONNECTIONS.inc()
    logger.info(f"Client connected: {request.sid}")
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    ACTIVE_CONNECTIONS.dec()
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('subscribe_ticker')
def handle_ticker_subscription(data):
    try:
        ticker = data.get('ticker', '').upper()
        if ticker:
            from flask_socketio import join_room
            join_room(f"ticker_{ticker}")
            emit('subscription_confirmed', {
                'ticker': ticker,
                'status': 'subscribed'
            })
            logger.info(f"Client {request.sid} subscribed to {ticker}")
    except Exception as e:
        logger.error(f"Subscription error: {e}")
        emit('error', {'message': 'Subscription failed'})

def background_price_updates():
    popular_tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META']

    while True:
        try:
            for ticker in popular_tickers:
                price_data = data_fetcher.get_latest_price(ticker)

                if price_data:
                    socketio.emit('price_update', {
                        'ticker': ticker,
                        'price': price_data['price'],
                        'change': price_data.get('change', 0),
                        'change_percent': price_data.get('change_percent', 0),
                        'timestamp': datetime.now().isoformat()
                    }, room=f"ticker_{ticker}")

            time.sleep(30)

        except Exception as e:
            logger.error(f"Background update error: {e}")
            time.sleep(60)

def start_background_tasks():
    update_thread = threading.Thread(target=background_price_updates, daemon=True)
    update_thread.start()
    logger.info("Background tasks started")

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    start_background_tasks()
    socketio.run(
        app,
        debug=os.getenv('FLASK_ENV') == 'development',
        host='0.0.0.0',
        port=5000
    )
