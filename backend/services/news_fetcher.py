import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(symbol):
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["articles"]
    else:
        return []