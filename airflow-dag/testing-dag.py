import json, pathlib, airflow, requests, os
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="test",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None,
)
download = BashOperator(
    task_id="download",
    bash_command="curl -o ./launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming' && ls -la && pwd",
    dag = dag,
)

def _get_pictures():
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
    os.system("pwd && ls -la")

get_pictures = PythonOperator(
    task_id="get_pictures", python_callable=_get_pictures, dag=dag
)


download >> get_pictures