from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime


def list_s3_objects():
    hook = S3Hook(aws_conn_id="aws_default")
    bucket = "persistance-nov-bucket"
    keys = hook.list_keys(bucket_name=bucket)
    print("Files:", keys)


with DAG(
    dag_id="example_s3_hook",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    list_task = PythonOperator(
        task_id="list_s3_files",
        python_callable=list_s3_objects
    )
