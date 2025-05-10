import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pymongo
import redis
import json
from bson import ObjectId

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://root:password123@localhost:27017/stockprediction?authSource=admin')
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.db = self.mongo_client.stockprediction

        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis_client = redis.from_url(redis_url, decode_responses=True)

        self._initialize_collections()

    def _initialize_collections(self):
        try:
            self.db.stock_prices.create_index([("ticker", 1), ("timestamp", -1)])
            self.db.stock_prices.create_index([("timestamp", -1)])
            self.db.news_sentiment.create_index([("ticker", 1), ("timestamp", -1)])
            self.db.news_sentiment.create_index([("timestamp", -1)])
            self.db.predictions.create_index([("ticker", 1), ("timestamp", -1)])
            self.db.predictions.create_index([("timestamp", -1)])

            logger.info("Database collections initialized")
        except Exception as e:
            logger.error(f"Failed to initialize collections: {e}")

    def health_check(self) -> Dict:
        try:
            mongo_status = self.mongo_client.admin.command('ping')
            redis_status = self.redis_client.ping()

            return {
                "mongodb": "healthy" if mongo_status else "unhealthy",
                "redis": "healthy" if redis_status else "unhealthy"
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"mongodb": "unhealthy", "redis": "unhealthy"}

    def store_stock_data(self, ticker: str, data: Dict) -> bool:
        try:
            data['ticker'] = ticker
            data['timestamp'] = datetime.utcnow()

            result = self.db.stock_prices.insert_one(data)

            cache_key = f"stock:{ticker}:latest"
            self.redis_client.setex(cache_key, 3600, json.dumps(data, default=str))

            logger.debug(f"Stored stock data for {ticker}")
            return bool(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to store stock data: {e}")
            return False

    def get_stock_history(self, ticker: str, start_date: datetime, 
                         end_date: datetime, page: int = 1, limit: int = 100) -> List[Dict]:
        try:
            skip = (page - 1) * limit

            cursor = self.db.stock_prices.find({
                "ticker": ticker,
                "timestamp": {"$gte": start_date, "$lte": end_date}
            }).sort("timestamp", -1).skip(skip).limit(limit)

            data = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                data.append(doc)

            return data
        except Exception as e:
            logger.error(f"Failed to get stock history: {e}")
            return []

    def store_sentiment_data(self, ticker: str, sentiment_data: Dict) -> bool:
        try:
            sentiment_data['ticker'] = ticker
            sentiment_data['timestamp'] = datetime.utcnow()

            result = self.db.news_sentiment.insert_one(sentiment_data)

            cache_key = f"sentiment:{ticker}:latest"
            self.redis_client.setex(cache_key, 900, json.dumps(sentiment_data, default=str))

            return bool(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to store sentiment data: {e}")
            return False

    def get_sentiment_data(self, ticker: str, hours: int = 24) -> Dict:
        try:
            cache_key = f"sentiment:{ticker}:aggregated"
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            start_time = datetime.utcnow() - timedelta(hours=hours)

            pipeline = [
                {"$match": {
                    "ticker": ticker,
                    "timestamp": {"$gte": start_time}
                }},
                {"$group": {
                    "_id": None,
                    "avg_sentiment": {"$avg": "$sentiment_score"},
                    "sentiment_count": {"$sum": 1},
                    "positive_count": {"$sum": {"$cond": [{"$gt": ["$sentiment_score", 0.1]}, 1, 0]}},
                    "negative_count": {"$sum": {"$cond": [{"$lt": ["$sentiment_score", -0.1]}, 1, 0]}},
                    "neutral_count": {"$sum": {"$cond": [
                        {"$and": [{"$gte": ["$sentiment_score", -0.1]}, {"$lte": ["$sentiment_score", 0.1]}]}, 1, 0
                    ]}}
                }}
            ]

            result = list(self.db.news_sentiment.aggregate(pipeline))

            if result:
                sentiment_summary = {
                    "avg_sentiment": result[0]["avg_sentiment"],
                    "total_articles": result[0]["sentiment_count"],
                    "positive_count": result[0]["positive_count"],
                    "negative_count": result[0]["negative_count"],
                    "neutral_count": result[0]["neutral_count"],
                    "hours": hours
                }

                self.redis_client.setex(cache_key, 600, json.dumps(sentiment_summary))
                return sentiment_summary
            else:
                return {
                    "avg_sentiment": 0.0,
                    "total_articles": 0,
                    "positive_count": 0,
                    "negative_count": 0,
                    "neutral_count": 0,
                    "hours": hours
                }
        except Exception as e:
            logger.error(f"Failed to get sentiment data: {e}")
            return {}

    def store_prediction(self, ticker: str, prediction_data: Dict) -> bool:
        try:
            prediction_data['ticker'] = ticker
            prediction_data['timestamp'] = datetime.utcnow()

            result = self.db.predictions.insert_one(prediction_data)

            cache_key = f"prediction:{ticker}:latest"
            self.redis_client.setex(cache_key, 300, json.dumps(prediction_data, default=str))

            return bool(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to store prediction: {e}")
            return False

    def get_latest_prediction(self, ticker: str) -> Optional[Dict]:
        try:
            cache_key = f"prediction:{ticker}:latest"
            cached = self.redis_client.get(cache_key)
            if cached:
                data = json.loads(cached)
                data['source'] = 'cache'
                return data

            doc = self.db.predictions.find_one(
                {"ticker": ticker},
                sort=[("timestamp", -1)]
            )

            if doc:
                doc['_id'] = str(doc['_id'])
                doc['source'] = 'database'
                return doc

            return None
        except Exception as e:
            logger.error(f"Failed to get latest prediction: {e}")
            return None

    def get_available_tickers(self) -> List[str]:
        try:
            cache_key = "tickers:available"
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            tickers = self.db.stock_prices.distinct("ticker")

            self.redis_client.setex(cache_key, 3600, json.dumps(tickers))

            return sorted(tickers)
        except Exception as e:
            logger.error(f"Failed to get available tickers: {e}")
            return []
