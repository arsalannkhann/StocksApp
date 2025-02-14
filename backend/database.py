from pymongo import MongoClient
from redis import Redis
from dotenv import load_dotenv
import os

class DatabaseManager:
    def __init__(self):
        load_dotenv()  # Load environment variables
        self._mongo_client = None
        self._redis_client = None

    def init_db(self):
        """Initialize MongoDB and Redis connections"""
        # Initialize MongoDB
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
        self._mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self._mongo_client.stock_database  # Use your database name

        # Create collections if they don't exist
        if "stocks" not in self.mongo_db.list_collection_names():
            self.mongo_db.create_collection("stocks")
        if "users" not in self.mongo_db.list_collection_names():
            self.mongo_db.create_collection("users")

        # Initialize Redis
        redis_url = os.getenv("REDIS_URL")
        if not redis_url:
            raise ValueError("REDIS_URL environment variable is not set")
        self._redis_client = Redis.from_url(redis_url)

    def close_db(self):
        """Close MongoDB and Redis connections"""
        if self._mongo_client:
            self._mongo_client.close()

        if self._redis_client:
            self._redis_client.connection_pool.disconnect()

# Create a singleton instance
db_manager = DatabaseManager()

def init_db():
    """Initialize database connections"""
    db_manager.init_db()

def close_db():
    """Close database connections"""
    db_manager.close_db()