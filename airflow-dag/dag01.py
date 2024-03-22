import json, pathlib, airflow, requests, os, subprocess, urllib.request
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from subprocess import Popen

dag = DAG(
    dag_id="download_rocket",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval=None,
)
download = BashOperator(
    task_id="download",
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming' && pwd && ls -la && cd /tmp/ && ls -la && pwd",
    dag = dag,
)

def _get_pictures():
    urllib.request.urlretrieve(url="https://ll.thespacedevs.com/2.0.0/launch/upcoming", filename="launches.json")
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
    subprocess.run(["pwd"], capture_output=True)
    print(subprocess.run(["pwd"], capture_output=True))
    subprocess.run(["ls", "-la"], capture_output=True)
    print(subprocess.run(["ls", "-la"], capture_output=True))
    subprocess.run(["ls", "/tmp"], capture_output=True)
    print(subprocess.run(["ls", "/tmp"], capture_output=True))
    # with open("launches.json") as f:
    #     launches= json.load(f)
    #     image_urls =[launch["image"] for launch in launches["results"]]
        
    #     for image_url in image_urls:
    #         try:
    #             response = requests.get(image_url)
    #             image_filename = image_url.split("/")[-1]
    #             target_file = f"./images/{image_filename}"
    #         except requests_exceptions.MissingSchema:
    #             print(f"{image_url} appears to be an invalid URL.")
    #         except requests_exceptions.ConnectionError:
    #             print(f"Could not connect to {image_url}.")

get_pictures = PythonOperator(
    task_id="get_pictures", python_callable=_get_pictures, dag=dag
)

notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are ... images." && cd /tmp && ls -la',
    dag=dag,
)

download >> get_pictures >> notify