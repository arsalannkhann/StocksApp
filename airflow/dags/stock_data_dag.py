from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pymongo
import redis
import os
import json

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_and_store_stock_data():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

    mongo_client = pymongo.MongoClient("mongodb://root:password123@mongodb:27017/")
    mongo_db = mongo_client["stockprediction"]
    redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

    for ticker in tickers:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={api_key}&outputsize=compact"
        response = requests.get(url)
        data = response.json().get("Time Series (5min)", {})

        transformed = [
            {
                "ticker": ticker,
                "timestamp": ts,
                "open": float(val["1. open"]),
                "high": float(val["2. high"]),
                "low": float(val["3. low"]),
                "close": float(val["4. close"]),
                "volume": int(val["5. volume"])
            }
            for ts, val in data.items()
        ]

        if transformed:
            mongo_db[ticker].insert_many(transformed)
            redis_client.set(f"{ticker}_latest", json.dumps(transformed[:10]))

with DAG(
    dag_id='stock_data_dag',
    default_args=default_args,
    schedule_interval='@hourly',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    fetch_stock = PythonOperator(
        task_id='fetch_and_store_stock_data',
        python_callable=fetch_and_store_stock_data
    )