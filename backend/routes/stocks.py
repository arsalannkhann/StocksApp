from flask import Blueprint, request, jsonify
from backend.utils.auth_utils import login_required

import requests
import os
from datetime import datetime
from backend.models.llama2_model import  Llama2Model
stocks_bp = Blueprint("stocks", __name__)

@stocks_bp.route("/analyze", methods=["GET"])
@login_required


def get_stock_data(symbol: str) -> dict:
    """Fetch latest stock data for a given symbol using Alpha Vantage API"""
    alpha_vantage_key = os.getenv("ALPHA_VANTAGE_KEY")
    
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": alpha_vantage_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "Time Series (5min)" not in data:
            return {"error": "Stock data not found"}
        
        latest_data = list(data["Time Series (5min)"].values())[0]
        return {
            "symbol": symbol,
            "last_close": float(latest_data["4. close"]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e)}
import requests
import os
from datetime import datetime, timedelta

def get_stock_news(symbol: str) -> list:
    """Fetch latest news articles for a given stock symbol using NewsAPI"""
    news_api_key = os.getenv("NEWS_API_KEY")
    
    url = f"https://newsapi.org/v2/everything"
    to_date = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    params = {
        "q": symbol,
        "from": from_date,
        "to": to_date,
        "sortBy": "relevancy",
        "language": "en",
        "apiKey": news_api_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("status") != "ok":
            return []
        
        return [
            {
                "title": article["title"],
                "description": article.get("description", ""),
                "source": article["source"]["name"],
                "url": article["url"]
            }
            for article in data["articles"][:5]  # Limit to 5 articles
        ]
    except Exception as e:
        return []
def analyze_stock(current_user):
    symbol = request.args.get("symbol", "").upper().strip()
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        # Implement stock data and news retrieval
        stock_data = get_stock_data(symbol)  # Implement this function
        news = get_stock_news(symbol)  # Implement this function

        model = Llama2Model()
        prompt = f"Stock {symbol} data: {stock_data}. News: {news}"
        prediction = model.generate_prediction(prompt)

        return jsonify({
            "stock_data": stock_data,
            "news": news,
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500