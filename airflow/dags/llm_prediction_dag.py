from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pymongo
import os
import sys
sys.path.append("/opt/airflow")

from ml_models.ensemble_predictor import get_prediction

import mlflow

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_batch_predictions():
    mongo_client = pymongo.MongoClient("mongodb://root:password123@mongodb:27017/")
    db = mongo_client["stockprediction"]
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

    for ticker in tickers:
        result = get_prediction(ticker)
        if result:
            db["predictions"].insert_one({
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                **result
            })

            mlflow.log_metric("confidence", result.get("confidence", 0.0))
            mlflow.log_metric("trend", 1 if result.get("trend") == "Up" else 0)

with DAG(
    dag_id='llm_prediction_dag',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    predict = PythonOperator(
        task_id='run_batch_predictions',
        python_callable=run_batch_predictions
    )