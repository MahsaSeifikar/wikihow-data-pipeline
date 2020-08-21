from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from src.analysis.wikihow_text_analysis import analyze_posts


args = {
    'start_date': datetime(year=2020, month=7, day=21,
                         hour=22, minute=0, second=0),
    'provide_context': True,
}

dag = DAG(
    dag_id='wikihow_trend_analysis',
    schedule_interval='@daily',
    default_args=args,
    max_active_runs=1
)

analyzer = PythonOperator(
    task_id='analyze_trend_posts',
    python_callable=analyze_posts,
     op_kwargs={
        'processed_data_path': f'/wikihow_data_pipeline/data/processed/'
                               f'wikihow_trend/',
    },
    templates_dict={'run_time': "{{ ds }}"}, 
    dag=dag
)

# Dag
analyzer 





