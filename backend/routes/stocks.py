from flask import Blueprint, jsonify
from services.stock_data import get_real_time_stock_prices
from services.news_fetcher import fetch_latest_news

stocks_bp = Blueprint("stocks", __name__)

@stocks_bp.route("/prices", methods=["GET"])
def stock_prices():
    data = get_real_time_stock_prices()
    return jsonify(data)

@stocks_bp.route("/news", methods=["GET"])
def stock_news():
    data = fetch_latest_news()
    return jsonify(data)