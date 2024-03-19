import json, pathlib, airflow, requests, os
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="download_rocket",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None,
)
download = BashOperator(
    task_id="download",
    bash_command="curl -o ./launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming' && ls -la",
    dag = dag,
)

def _get_pictures():
    pathlib.Path("./images").mkdir(parents=True, exist_ok=True)
    
    with open("./launches.json") as f:
        launches= json.load(f)
        image_urls =[launch["image"] for launch in launches["results"]]
        
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"./images/{image_filename}"
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")

get_pictures = PythonOperator(
    task_id="get_pictures", python_callable=_get_pictures, dag=dag
)

notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are now $(ls ./images/ | wc -l) images."',
    dag=dag,
)

download >> get_pictures >> notify