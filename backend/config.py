import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    MONGO_URI = os.getenv("MONGO_URI")
    REDIS_URL = os.getenv("REDIS_URL")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

config = Config()