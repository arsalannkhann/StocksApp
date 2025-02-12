from flask import Blueprint, jsonify
from backend.services.stock_data import get_stock_prices
from backend.services.news_fetcher import fetch_latest_news

stocks_bp = Blueprint("stocks", __name__)

@stocks_bp.route("/prices", methods=["GET"])
def stock_prices():
    data = get_stock_prices()
    return jsonify(data)

@stocks_bp.route("/news", methods=["GET"])
def stock_news():
    data = fetch_latest_news()
    return jsonify(data)