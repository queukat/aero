from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from cannabis_data_fetcher import fetch_data_from_api, store_data_to_postgres 

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'cannabis_data_dag',
    default_args=default_args,
    description='Fetch cannabis data and store it in PostgreSQL',
    schedule_interval=timedelta(hours=12),
    start_date=datetime(2023, 10, 26),
    catchup=False,
)


def fetch_and_store():
    data = fetch_data_from_api()
    if data:
        store_data_to_postgres(data)

fetch_and_store_task = PythonOperator(
    task_id='fetch_and_store_task',
    python_callable=fetch_and_store,
    dag=dag,
)

fetch_and_store_task
