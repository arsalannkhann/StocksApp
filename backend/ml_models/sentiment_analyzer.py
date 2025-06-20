import logging
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FinancialSentimentAnalyzer:
    def __init__(self, model_name="ahmedrachid/FinancialBERT-Sentiment-Analysis"):
        self.model_name = model_name
        self.sentiment_pipeline = None

        self.sentiment_map = {
            'positive': 1.0,
            'neutral': 0.0,
            'negative': -1.0,
            'POSITIVE': 1.0,
            'NEUTRAL': 0.0,
            'NEGATIVE': -1.0
        }

        self._initialize_model()

    def _initialize_model(self):
        try:
            # Try to initialize with HuggingFace
            # from transformers import pipeline
            # self.sentiment_pipeline = pipeline("sentiment-analysis", model=self.model_name)
            logger.info(f"Sentiment analyzer initialized with mock model")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment model: {e}")
            self.sentiment_pipeline = None

    def analyze_text(self, text: str) -> Dict:
        if not self.sentiment_pipeline:
            return self._mock_sentiment(text)

        try:
            cleaned_text = self._preprocess_text(text)

            if not cleaned_text:
                return {
                    'sentiment': 'neutral',
                    'confidence': 0.5,
                    'score': 0.0,
                    'text': text
                }

            # Use mock sentiment for now
            return self._mock_sentiment(text)

        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return self._mock_sentiment(text)

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        results = []
        for text in texts:
            result = self.analyze_text(text)
            results.append(result)
        return results

    def _preprocess_text(self, text: str) -> str:
        if not text:
            return ""

        text = str(text).strip()
        text = text.replace('\n', ' ').replace('\r', ' ')

        if len(text) > 512:
            text = text[:512]

        return text

    def _mock_sentiment(self, text: str) -> Dict:
        positive_words = ['good', 'great', 'excellent', 'positive', 'up', 'gain', 'profit', 'strong']
        negative_words = ['bad', 'poor', 'negative', 'down', 'loss', 'weak', 'decline', 'fall']

        text_lower = text.lower()

        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)

        if pos_count > neg_count:
            sentiment = 'positive'
            score = 0.7
        elif neg_count > pos_count:
            sentiment = 'negative'
            score = -0.7
        else:
            sentiment = 'neutral'
            score = 0.0

        return {
            'sentiment': sentiment,
            'confidence': 0.6,
            'score': score,
            'text': text
        }
