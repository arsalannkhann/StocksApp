import requests
from config import config

def fetch_latest_news():
    url = f"https://newsapi.org/v2/everything?q=stocks&apiKey={config.NEWS_API_KEY}"
    response = requests.get(url)
    return response.json()