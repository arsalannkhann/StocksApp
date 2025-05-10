import logging
import numpy as np
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EnsemblePredictor:
    def __init__(self, lstm_model, sentiment_analyzer, weights=(0.6, 0.4)):
        self.lstm_model = lstm_model
        self.sentiment_analyzer = sentiment_analyzer
        self.weights = weights
        self.model_version = "1.0.0"

    def predict(self, ticker: str, price_data: np.ndarray, sentiment_data: Dict) -> Optional[Dict]:
        try:
            lstm_prediction = self.lstm_model.predict(price_data)
            lstm_confidence = self._calculate_lstm_confidence(price_data)

            sentiment_adjustment, sentiment_confidence = self._calculate_sentiment_adjustment(
                sentiment_data, price_data
            )

            if isinstance(lstm_prediction, (list, np.ndarray)):
                base_price = float(lstm_prediction[0] if len(lstm_prediction) > 0 else lstm_prediction)
            else:
                base_price = float(lstm_prediction)

            sentiment_adjusted_price = base_price * (1 + sentiment_adjustment)

            final_prediction = (
                self.weights[0] * base_price + 
                self.weights[1] * sentiment_adjusted_price
            )

            overall_confidence = (
                self.weights[0] * lstm_confidence + 
                self.weights[1] * sentiment_confidence
            )

            current_price = price_data[-1] if len(price_data) > 0 else base_price
            price_change = final_prediction - current_price
            trend = "up" if price_change > 0 else "down" if price_change < 0 else "flat"

            return {
                'ticker': ticker,
                'predicted_price': round(float(final_prediction), 2),
                'confidence': round(float(overall_confidence), 3),
                'lstm_prediction': round(float(base_price), 2),
                'sentiment_adjustment': round(float(sentiment_adjustment), 4),
                'sentiment_score': sentiment_data.get('avg_sentiment', 0.0),
                'trend': trend,
                'price_change': round(float(price_change), 2),
                'price_change_percent': round(float(price_change / current_price * 100), 2),
                'model_components': {
                    'lstm_weight': self.weights[0],
                    'sentiment_weight': self.weights[1],
                    'lstm_confidence': round(float(lstm_confidence), 3),
                    'sentiment_confidence': round(float(sentiment_confidence), 3)
                },
                'timestamp': datetime.now().isoformat(),
                'model_version': self.model_version
            }

        except Exception as e:
            logger.error(f"Ensemble prediction error for {ticker}: {e}")
            return self._fallback_prediction(ticker, price_data, sentiment_data)

    def _calculate_lstm_confidence(self, price_data: np.ndarray) -> float:
        try:
            if len(price_data) < 10:
                return 0.5

            returns = np.diff(price_data) / price_data[:-1]
            volatility = np.std(returns)

            trend_consistency = self._calculate_trend_consistency(price_data)

            volatility_confidence = max(0.3, 1.0 - (volatility * 10))

            confidence = (volatility_confidence * 0.7) + (trend_consistency * 0.3)

            return min(0.95, max(0.3, confidence))

        except Exception as e:
            logger.error(f"LSTM confidence calculation error: {e}")
            return 0.5

    def _calculate_trend_consistency(self, price_data: np.ndarray) -> float:
        try:
            if len(price_data) < 5:
                return 0.5

            recent_data = price_data[-10:]

            differences = np.diff(recent_data)
            direction_changes = np.sum(np.diff(np.sign(differences)) != 0)

            max_possible_changes = len(recent_data) - 2
            if max_possible_changes <= 0:
                return 0.5

            consistency = 1.0 - (direction_changes / max_possible_changes)
            return max(0.0, min(1.0, consistency))

        except Exception as e:
            logger.error(f"Trend consistency calculation error: {e}")
            return 0.5

    def _calculate_sentiment_adjustment(self, sentiment_data: Dict, price_data: np.ndarray) -> tuple:
        try:
            if not sentiment_data or 'avg_sentiment' not in sentiment_data:
                return 0.0, 0.5

            avg_sentiment = sentiment_data['avg_sentiment']
            total_articles = sentiment_data.get('total_articles', 0)
            confidence_avg = sentiment_data.get('confidence_avg', 0.5)

            base_adjustment = avg_sentiment * 0.02

            volume_factor = min(1.0, total_articles / 10)

            adjustment = avg_sentiment * 0.02 * volume_factor

            sentiment_confidence = min(0.9, (volume_factor * 0.6) + (confidence_avg * 0.4))

            return adjustment, sentiment_confidence

        except Exception as e:
            logger.error(f"Sentiment adjustment calculation error: {e}")
            return 0.0, 0.5

    def _fallback_prediction(self, ticker: str, price_data: np.ndarray, sentiment_data: Dict) -> Dict:
        try:
            if len(price_data) > 0:
                current_price = float(price_data[-1])

                if len(price_data) > 1:
                    recent_change = price_data[-1] - price_data[-2]
                    trend_prediction = current_price + (recent_change * 0.5)
                else:
                    trend_prediction = current_price * 1.001

                sentiment_score = sentiment_data.get('avg_sentiment', 0.0) if sentiment_data else 0.0
                sentiment_adjustment = sentiment_score * 0.01

                final_prediction = trend_prediction * (1 + sentiment_adjustment)

                return {
                    'ticker': ticker,
                    'predicted_price': round(float(final_prediction), 2),
                    'confidence': 0.4,
                    'lstm_prediction': round(float(trend_prediction), 2),
                    'sentiment_adjustment': round(float(sentiment_adjustment), 4),
                    'sentiment_score': sentiment_score,
                    'trend': "up" if final_prediction > current_price else "down",
                    'price_change': round(float(final_prediction - current_price), 2),
                    'price_change_percent': round(float((final_prediction - current_price) / current_price * 100), 2),
                    'model_components': {
                        'lstm_weight': 0.8,
                        'sentiment_weight': 0.2,
                        'lstm_confidence': 0.4,
                        'sentiment_confidence': 0.3
                    },
                    'timestamp': datetime.now().isoformat(),
                    'model_version': f"{self.model_version}-fallback",
                    'fallback': True
                }
            else:
                return {
                    'ticker': ticker,
                    'predicted_price': 100.0,
                    'confidence': 0.1,
                    'lstm_prediction': 100.0,
                    'sentiment_adjustment': 0.0,
                    'sentiment_score': 0.0,
                    'trend': "flat",
                    'price_change': 0.0,
                    'price_change_percent': 0.0,
                    'model_components': {
                        'lstm_weight': 1.0,
                        'sentiment_weight': 0.0,
                        'lstm_confidence': 0.1,
                        'sentiment_confidence': 0.1
                    },
                    'timestamp': datetime.now().isoformat(),
                    'model_version': f"{self.model_version}-minimal-fallback",
                    'fallback': True,
                    'error': "Insufficient data for prediction"
                }

        except Exception as e:
            logger.error(f"Fallback prediction error: {e}")
            return {
                'ticker': ticker,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
