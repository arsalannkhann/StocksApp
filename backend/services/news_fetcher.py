import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API Key from .env file
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

logger = logging.getLogger(__name__)


def fetch_latest_news(symbol: str):
    """
    Fetches the latest financial news related to the given stock symbol.

    Args:
        symbol (str): The stock symbol (e.g., AAPL, TSLA).

    Returns:
        list: A list of news articles (each article is a dictionary).
    """
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY is missing. Check your .env file.")
        return []

    try:
        params = {
            "q": symbol,  # Search for articles related to the stock symbol
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
        }

        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        news_data = response.json()

        return news_data.get("articles", [])

    except requests.RequestException as e:
        logger.error(f"Error fetching news for {symbol}: {e}")
        return []