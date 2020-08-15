from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.etl.wikihow_trend_etl import run_etl


def get_yesterday_date():
    return (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")


args = {
    'start_date': datetime(year=2020, month=7, day=10,
                         hour=23, minute=0, second=0),
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
        'raw_data_path': f'/wikihow_data_pipeline/data/raw/wikihow_trend/'
                            f'{get_yesterday_date()}',
        'processed_data_path': f'/wikihow_data_pipeline/data/processed/'
                               f'wikihow_trend/{get_yesterday_date()}',
    },
    dag=dag
)

etl 
