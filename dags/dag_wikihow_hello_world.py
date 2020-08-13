from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator


args = {
    'start_date': datetime(year=2019, month=12, day=22,
                         hour=23, minute=0, second=0),
    'provide_context': True,
}

dag = DAG(
    dag_id='wikihow_hello_world',
    schedule_interval='@daily',
    default_args=args,
    max_active_runs=1
)

hello_world = BashOperator(
    task_id = 'wikihow_hello_world',
    bash_command = "echo Hello World!",
    dag = dag
)

hello_world 





