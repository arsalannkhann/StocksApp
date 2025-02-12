import redis
import json
from backend.config import config
from backend.services.stock_api import get_stock_prices
from backend.services.news_fetcher import fetch_latest_news as fetch_news

from backend.models.llama2_model import predict_stock_trend

redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)

import redis
import json
import logging
from functools import wraps


def handle_cache_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except redis.exceptions.RedisError as e:
            logging.error(f"Redis cache error: {e}")
            return None

    return wrapper


class StockDataFetcher:
    def __init__(self, redis_client, cache_duration=300):
        self.redis_client = redis_client
        self.cache_duration = cache_duration
        self.logger = logging.getLogger(__name__)

    @handle_cache_errors
    def fetch_stock_prices_cached(self, symbol):
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Invalid stock symbol")

        cache_key = f"stock:{symbol.upper()}"
        cached_data = self.redis_client.get(cache_key)

        if cached_data:
            try:
                return json.loads(cached_data)
            except json.JSONDecodeError:
                self.logger.warning(f"Invalid cached data for {symbol}")

        try:
            stock_data = get_stock_prices(symbol)
            self.redis_client.setex(cache_key, self.cache_duration, json.dumps(stock_data))
            return stock_data
        except Exception as e:
            self.logger.error(f"Stock price fetch error for {symbol}: {e}")
            return None

    def get_stock_analysis(self, symbol):
        try:
            stock_data = self.fetch_stock_prices_cached(symbol)
            news_articles = fetch_news(symbol)

            if not stock_data or not news_articles:
                return {
                    "error": "Unable to fetch complete stock information"
                }

            prediction = predict_stock_trend(stock_data, news_articles)

            return {
                "stock_data": stock_data,
                "news": news_articles,
                "prediction": prediction
            }
        except Exception as e:
            self.logger.error(f"Stock analysis error for {symbol}: {e}")
            return {"error": str(e)}
