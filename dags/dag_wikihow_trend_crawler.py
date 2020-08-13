from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator



args = {
    'start_date': datetime(year=2020, month=7, day=10,
                         hour=0, minute=0, second=0),
    'provide_context': True,
}

dag = DAG(
    dag_id='wikihow_trend_crawler',
    schedule_interval='@daily',
    default_args=args,
    max_active_runs=1
)

crawler = BashOperator(
    task_id = 'crawler',
    bash_command = "scrapy runspider /wikihow_data_pipeline/dags/crawler/wikihow_scraper.py",
    dag = dag
)


crawler 





