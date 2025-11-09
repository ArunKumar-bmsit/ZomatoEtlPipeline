from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data


default_args = {
    'owner': 'airflow',
    'retries': 1,
}

with DAG(
    dag_id='zomato_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 11, 1),
    schedule_interval=None,
    catchup=False,
    description='ETL pipeline for Zomato dataset with star schema',
) as dag:

    # Extract task
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    # Transform task
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    # Load task
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    # Define dependencies (Extract → Transform → Load)
    extract_task >> transform_task >> load_task
