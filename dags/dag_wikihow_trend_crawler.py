from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from src.crawler.wikihow_scraper import run_crawler


args = {
    'start_date': datetime(year=2020, month=7, day=10,
                         hour=22, minute=0, second=0),
    'provide_context': True,
}

dag = DAG(
    dag_id='wikihow_trend_crawler',
    schedule_interval='@daily',
    default_args=args,
    max_active_runs=1
)

crawler = PythonOperator(
    task_id='crawler_trend_posts',
    python_callable=run_crawler,
    dag=dag
)

# Dag
crawler 





