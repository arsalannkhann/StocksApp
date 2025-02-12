import json
import logging
from backend.models.llama2_model import predict_stock_trend

logger = logging.getLogger(__name__)

def predict_stock(symbol: str):
    try:
        # Load historical stock data and latest news
        from backend.services.stock_data import get_stock_prices
        from backend.services.news_fetcher import fetch_latest_news

        stock_data = get_stock_prices(symbol)
        news_articles = fetch_latest_news(symbol)

        if not stock_data or not news_articles:
            return "Insufficient data for prediction"

        # Predict stock trend using Llama2
        prediction = predict_stock_trend(stock_data, news_articles)

        return prediction
    except Exception as e:
        logger.error(f"Stock prediction error for {symbol}: {e}")
        return "Prediction failed due to an error"