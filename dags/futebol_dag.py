import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path

from src.extract import extract_standings
from src.transform import transform_to_parquet
from src.load import upload_to_s3

# 🔑 API KEY vem do .env
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
BUCKET = os.getenv("S3_BUCKET")

BASE_PATH = Path("/opt/airflow/data")
RAW_PATH = BASE_PATH / "raw"
TRUSTED_PATH = BASE_PATH / "trusted"

RAW_PATH.mkdir(parents=True, exist_ok=True)
TRUSTED_PATH.mkdir(parents=True, exist_ok=True)


def extract_task(**context):
    date = context["ds"]
    return extract_standings(
        api_key=API_KEY,
        out_json_path=str(RAW_PATH / f"dados_{date}.json")
    )


def transform_task(**context):
    date = context["ds"]
    in_json = str(RAW_PATH / f"dados_{date}.json")
    out_parquet = str(TRUSTED_PATH / f"classificacao_{date}.parquet")
    return transform_to_parquet(in_json, out_parquet)


def load_task(**context):
    date = context["ds"]
    parquet = str(TRUSTED_PATH / f"classificacao_{date}.parquet")
    upload_to_s3(
        local_path=parquet,
        bucket=BUCKET,
        s3_key=f"trusted/airflow/dt={date}/classificacao.parquet"
    )


with DAG(
    dag_id="futebol_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="extract", python_callable=extract_task)
    t2 = PythonOperator(task_id="transform", python_callable=transform_task)
    t3 = PythonOperator(task_id="load", python_callable=load_task)

    t1 >> t2 >> t3
