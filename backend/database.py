from pymongo import MongoClient
import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client.stock_database
        self.redis = Redis.from_url(os.getenv("REDIS_URL"))

    def get_stock_data(self, symbol):
        return self.db.stocks.find_one({"symbol": symbol})

db = Database()