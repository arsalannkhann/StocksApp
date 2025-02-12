import redis
import json
from config import config
from .stock_api import get_stock_prices

redis_client = redis.Redis.from_url(config.REDIS_URL, decode_responses=True)


def get_real_time_stock_prices(symbols=None):
    """
    Fetch real-time stock prices, with optional symbol filtering

    :param symbols: Optional list of stock symbols to fetch
    :return: Dictionary of stock prices
    """
    # If no symbols provided, you might want to define a default list
    if symbols is None:
        symbols = ['AAPL', 'GOOGL', 'MSFT']

    stock_prices = {}
    for symbol in symbols:
        stock_prices[symbol] = fetch_stock_prices_cached(symbol)

    return stock_prices


def fetch_stock_prices_cached(symbol):
    cache_key = f"stock:{symbol}"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)  # Return cached result

    # If not cached, fetch fresh data
    stock_data = get_stock_prices(symbol)

    # Store in Redis for 5 minutes (300 seconds)
    redis_client.setex(cache_key, 300, json.dumps(stock_data))

    return stock_data