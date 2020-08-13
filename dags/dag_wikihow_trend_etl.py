from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.etl.wikihow_trend_etl import run_etl

args = {
    'start_date': datetime(year=2020, month=7, day=10,
                         hour=0, minute=0, second=0),
    'provide_context': True,
}

dag = DAG(
    dag_id='wikihow_trend_etl',
    schedule_interval='@daily',
    default_args=args,
    max_active_runs=1
)

etl = PythonOperator(
    task_id='trend_etl',
    python_callable=run_etl,
    op_kwargs={
        'project_name': 'wikihow_trend',
    },
    dag=dag
)

etl 
