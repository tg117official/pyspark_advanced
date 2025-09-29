from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define basic Python callables
def extract():
    print("Extracting data...")

def transform():
    print("Transforming data...")

def load():
    print("Loading data...")

# Define default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

# Define the DAG
with DAG(
    dag_id='basic_etl_demo',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='A simple ETL demo DAG with 5 tasks'
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load
    )

    end = DummyOperator(
        task_id='end'
    )

    # Set task dependencies
    start >> extract_data >> transform_data >> load_data >> end
