from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pymongo
import os

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_news_and_sentiment():
    finnhub_api = os.getenv("FINNHUB_API_KEY")
    hf_token = os.getenv("HF_TOKEN")
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

    mongo_client = pymongo.MongoClient("mongodb://root:password123@mongodb:27017/")
    mongo_db = mongo_client["stockprediction"]

    for ticker in tickers:
        url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-01-01&to=2025-12-31&token={finnhub_api}"
        news = requests.get(url).json()

        for article in news[:10]:
            headline = article.get("headline", "")
            payload = {
                "inputs": headline
            }
            response = requests.post(
                "https://api-inference.huggingface.co/models/finance_sentiment_model",
                headers={"Authorization": f"Bearer {hf_token}"},
                json=payload
            )
            sentiment = response.json()

            mongo_db["sentiment"].insert_one({
                "ticker": ticker,
                "headline": headline,
                "sentiment": sentiment,
                "timestamp": datetime.now().isoformat()
            })

with DAG(
    dag_id='news_sentiment_dag',
    default_args=default_args,
    schedule_interval='*/15 * * * *',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    fetch_news = PythonOperator(
        task_id='fetch_news_and_sentiment',
        python_callable=fetch_news_and_sentiment
    )