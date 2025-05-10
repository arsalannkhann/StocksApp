import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging
import os

logger = logging.getLogger(__name__)

class StockLSTM:
    def __init__(self, lookback_window=60, lstm_units=[128, 64, 32]):
        self.lookback_window = lookback_window
        self.lstm_units = lstm_units
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.is_trained = False

    def prepare_data(self, data):
        if len(data) < self.lookback_window + 1:
            raise ValueError(f"Insufficient data: need at least {self.lookback_window + 1} points")

        scaled_data = self.scaler.fit_transform(data.reshape(-1, 1))

        X, y = [], []
        for i in range(self.lookback_window, len(scaled_data)):
            X.append(scaled_data[i-self.lookback_window:i, 0])
            y.append(scaled_data[i, 0])

        X, y = np.array(X), np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))

        return X, y

    def predict(self, data, steps_ahead=1):
        if not self.is_trained or self.model is None:
            logger.warning("Model not trained yet, returning mock prediction")
            return self._mock_prediction(data)

        try:
            if len(data) < self.lookback_window:
                logger.warning(f"Insufficient data for prediction: {len(data)} < {self.lookback_window}")
                return self._mock_prediction(data)

            recent_data = data[-self.lookback_window:]
            scaled_data = self.scaler.transform(recent_data.reshape(-1, 1))

            X = scaled_data.reshape((1, self.lookback_window, 1))

            predictions = []
            current_input = X

            for _ in range(steps_ahead):
                pred_scaled = self.model.predict(current_input, verbose=0)
                pred_actual = self.scaler.inverse_transform(pred_scaled)
                predictions.append(float(pred_actual[0][0]))

                if steps_ahead > 1:
                    current_input = np.roll(current_input, -1, axis=1)
                    current_input[0, -1, 0] = pred_scaled[0][0]

            return predictions[0] if steps_ahead == 1 else predictions

        except Exception as e:
            logger.error(f"LSTM prediction error: {e}")
            return self._mock_prediction(data)

    def _mock_prediction(self, data):
        if len(data) > 0:
            last_price = data[-1]
            trend = 0.001 if len(data) > 1 and data[-1] > data[-2] else -0.001
            mock_pred = last_price * (1 + trend + np.random.normal(0, 0.01))
            return float(mock_pred)
        return 100.0
