import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import time
import random

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.finnhub_key = os.getenv('FINNHUB_API_KEY')
        self.polygon_key = os.getenv('POLYGON_API_KEY')

        self.last_request_time = {}
        self.min_request_interval = 12

    def _rate_limit(self, api_name: str):
        current_time = time.time()
        if api_name in self.last_request_time:
            time_since_last = current_time - self.last_request_time[api_name]
            if time_since_last < self.min_request_interval:
                sleep_time = self.min_request_interval - time_since_last
                time.sleep(sleep_time)

        self.last_request_time[api_name] = time.time()

    def get_stock_data(self, ticker: str) -> Optional[Dict]:
        if not self.alpha_vantage_key:
            logger.warning("Alpha Vantage API key not provided, using mock data")
            return self._get_mock_stock_data(ticker)

        try:
            self._rate_limit('alpha_vantage')

            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': ticker,
                'interval': '5min',
                'apikey': self.alpha_vantage_key,
                'outputsize': 'compact'
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if 'Error Message' in data:
                logger.error(f"Alpha Vantage error: {data['Error Message']}")
                return self._get_mock_stock_data(ticker)

            if 'Note' in data:
                logger.warning(f"Alpha Vantage rate limit: {data['Note']}")
                return self._get_mock_stock_data(ticker)

            time_series = data.get('Time Series (5min)', {})
            if not time_series:
                logger.warning(f"No time series data for {ticker}")
                return self._get_mock_stock_data(ticker)

            latest_time = max(time_series.keys())
            latest_data = time_series[latest_time]

            return {
                'ticker': ticker,
                'timestamp': datetime.strptime(latest_time, '%Y-%m-%d %H:%M:%S'),
                'open_price': float(latest_data['1. open']),
                'high_price': float(latest_data['2. high']),
                'low_price': float(latest_data['3. low']),
                'close_price': float(latest_data['4. close']),
                'volume': int(latest_data['5. volume']),
                'source': 'alpha_vantage'
            }

        except Exception as e:
            logger.error(f"Alpha Vantage API error for {ticker}: {e}")
            return self._get_mock_stock_data(ticker)

    def get_latest_price(self, ticker: str) -> Optional[Dict]:
        try:
            stock_data = self.get_stock_data(ticker)
            if stock_data:
                base_price = stock_data['close_price']
                variation = random.uniform(-0.02, 0.02)
                current_price = base_price * (1 + variation)

                return {
                    'ticker': ticker,
                    'price': round(current_price, 2),
                    'change': round(current_price - base_price, 2),
                    'change_percent': round(variation * 100, 2),
                    'timestamp': datetime.now().isoformat()
                }

            return self._get_mock_latest_price(ticker)

        except Exception as e:
            logger.error(f"Latest price fetch error for {ticker}: {e}")
            return self._get_mock_latest_price(ticker)

    def _get_mock_stock_data(self, ticker: str) -> Dict:
        base_prices = {
            'AAPL': 180.0, 'GOOGL': 140.0, 'MSFT': 380.0, 'TSLA': 250.0,
            'AMZN': 150.0, 'NVDA': 480.0, 'META': 320.0
        }

        base_price = base_prices.get(ticker, 100.0)
        variation = random.uniform(-0.05, 0.05)

        current_price = base_price * (1 + variation)
        open_price = current_price * random.uniform(0.98, 1.02)
        high_price = max(open_price, current_price) * random.uniform(1.0, 1.03)
        low_price = min(open_price, current_price) * random.uniform(0.97, 1.0)

        return {
            'ticker': ticker,
            'timestamp': datetime.now(),
            'open_price': round(open_price, 2),
            'high_price': round(high_price, 2),
            'low_price': round(low_price, 2),
            'close_price': round(current_price, 2),
            'volume': random.randint(1000000, 50000000),
            'source': 'mock_data'
        }

    def _get_mock_latest_price(self, ticker: str) -> Dict:
        mock_data = self._get_mock_stock_data(ticker)
        return {
            'ticker': ticker,
            'price': mock_data['close_price'],
            'change': round(random.uniform(-5.0, 5.0), 2),
            'change_percent': round(random.uniform(-2.0, 2.0), 2),
            'timestamp': datetime.now().isoformat()
        }
