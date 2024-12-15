from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define the function for Task 1
def print_hello_world():
    print("Hello World")

# Define the function for Task 3
def print_goodbye():
    print("Goodbye")

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'hello_world_dag',
    default_args=default_args,
    description='A simple DAG with three tasks',
    schedule_interval=None,
)

# Task 1: Print "Hello World"
task_1 = PythonOperator(
    task_id='print_hello_world',
    python_callable=print_hello_world,
    dag=dag,
)

# Task 2: Echo "How are you"
task_2 = BashOperator(
    task_id='echo_how_are_you',
    bash_command='echo "How are you"',
    dag=dag,
)

# Task 3: Print "Goodbye"
task_3 = PythonOperator(
    task_id='print_goodbye',
    python_callable=print_goodbye,
    dag=dag,
)

# Set task dependencies
task_1 >> task_2 >> task_3
