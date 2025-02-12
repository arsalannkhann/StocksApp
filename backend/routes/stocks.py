from flask import Blueprint, request, jsonify
from backend.services.stock_data import get_stock_prices
from backend.services.news_fetcher import fetch_latest_news
from backend.services.stock_predictor import predict_stock

stocks_bp = Blueprint("stocks", __name__)


@stocks_bp.route("/analyze", methods=["GET"])
def analyze_stock():
    symbol = request.args.get("symbol", "").upper().strip()

    if not symbol:
        return jsonify({"error": "Stock symbol is required."}), 400

    try:
        # Fetch stock prices
        stock_data = get_stock_prices(symbol)

        # Fetch latest news
        news = fetch_latest_news(symbol)

        # Get stock price prediction
        prediction = predict_stock(symbol)

        return jsonify({
            "symbol": symbol,
            "stock_data": stock_data,
            "news": news,
            "prediction": prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500