import os
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import sys
sys.path.append('/app')

from ml_models.lstm_model import StockLSTM
from ml_models.sentiment_analyzer import FinancialSentimentAnalyzer
from ml_models.ensemble_predictor import EnsemblePredictor

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self, db_service):
        self.db_service = db_service
        self.lstm_model = StockLSTM()
        self.sentiment_analyzer = FinancialSentimentAnalyzer()
        self.ensemble_predictor = EnsemblePredictor(
            self.lstm_model,
            self.sentiment_analyzer
        )
        self.model_version = "1.0.0"

    def get_prediction(self, ticker: str, days_ahead: int = 1) -> Optional[Dict]:
        try:
            cached_prediction = self.db_service.get_latest_prediction(ticker)
            if cached_prediction and self._is_prediction_fresh(cached_prediction):
                return cached_prediction

            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)

            historical_data = self.db_service.get_stock_history(
                ticker, start_date, end_date, page=1, limit=1000
            )

            if len(historical_data) < 30:
                logger.warning(f"Insufficient data for {ticker}: {len(historical_data)} records")
                return self._generate_mock_prediction(ticker)

            sentiment_data = self.db_service.get_sentiment_data(ticker, hours=24)
            price_data = self._prepare_price_data(historical_data)

            prediction_result = self.ensemble_predictor.predict(
                ticker, price_data, sentiment_data
            )

            if prediction_result:
                prediction_data = {
                    **prediction_result,
                    'model_version': self.model_version,
                    'days_ahead': days_ahead,
                    'data_points_used': len(historical_data)
                }

                self.db_service.store_prediction(ticker, prediction_data)
                return prediction_data

            return self._generate_mock_prediction(ticker)

        except Exception as e:
            logger.error(f"Prediction generation error for {ticker}: {e}")
            return self._generate_mock_prediction(ticker)

    def _is_prediction_fresh(self, prediction: Dict, max_age_minutes: int = 15) -> bool:
        try:
            if isinstance(prediction['timestamp'], str):
                pred_time = datetime.fromisoformat(prediction['timestamp'].replace('Z', '+00:00'))
            else:
                pred_time = prediction['timestamp']

            age = datetime.now() - pred_time.replace(tzinfo=None)
            return age.total_seconds() < (max_age_minutes * 60)
        except Exception:
            return False

    def _prepare_price_data(self, historical_data: List[Dict]) -> np.ndarray:
        try:
            sorted_data = sorted(historical_data, key=lambda x: x['timestamp'])

            prices = []
            for record in sorted_data:
                if 'close_price' in record:
                    prices.append(float(record['close_price']))
                elif 'close' in record:
                    prices.append(float(record['close']))
                else:
                    logger.warning(f"No close price found in record: {record}")

            return np.array(prices)
        except Exception as e:
            logger.error(f"Data preparation error: {e}")
            return np.array([])

    def _generate_mock_prediction(self, ticker: str) -> Dict:
        import random

        base_prices = {
            'AAPL': 180.0, 'GOOGL': 140.0, 'MSFT': 380.0, 'TSLA': 250.0,
            'AMZN': 150.0, 'NVDA': 480.0, 'META': 320.0
        }

        base_price = base_prices.get(ticker, 100.0)
        variation = random.uniform(-0.03, 0.03)
        predicted_price = base_price * (1 + variation)

        price_change = predicted_price - base_price
        trend = "up" if price_change > 0 else "down" if price_change < 0 else "flat"

        return {
            'ticker': ticker,
            'predicted_price': round(predicted_price, 2),
            'confidence': round(random.uniform(0.6, 0.9), 3),
            'lstm_prediction': round(predicted_price * 0.7, 2),
            'sentiment_adjustment': round(variation * 0.3, 4),
            'sentiment_score': round(random.uniform(-0.2, 0.2), 3),
            'trend': trend,
            'price_change': round(price_change, 2),
            'price_change_percent': round((price_change / base_price) * 100, 2),
            'model_components': {
                'lstm_weight': 0.6,
                'sentiment_weight': 0.4,
                'lstm_confidence': round(random.uniform(0.6, 0.8), 3),
                'sentiment_confidence': round(random.uniform(0.5, 0.7), 3)
            },
            'timestamp': datetime.now().isoformat(),
            'model_version': self.model_version,
            'mock_data': True
        }
