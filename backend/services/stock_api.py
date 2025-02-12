import requests
import os
from config import config

def get_stock_prices(symbol):
    """
    Fetch real-time stock prices from Yahoo Finance or Alpha Vantage.
    """

    # Use Alpha Vantage API
    ALPHA_VANTAGE_API_KEY = config.ALPHA_VANTAGE_API_KEY
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()

        if "Time Series (5min)" in data:
            latest_timestamp = list(data["Time Series (5min)"].keys())[0]
            latest_data = data["Time Series (5min)"][latest_timestamp]

            return {
                "symbol": symbol,
                "timestamp": latest_timestamp,
                "open": float(latest_data["1. open"]),
                "high": float(latest_data["2. high"]),
                "low": float(latest_data["3. low"]),
                "close": float(latest_data["4. close"]),
                "volume": int(latest_data["5. volume"]),
            }

        else:
            return {"error": "Invalid API response", "details": data}

    except requests.exceptions.RequestException as e:
        return {"error": "API request failed", "details": str(e)}