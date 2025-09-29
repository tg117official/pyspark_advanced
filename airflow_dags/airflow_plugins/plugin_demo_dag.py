from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Importing the plugin-based operator
from hello_plugin import HelloOperator  # hello_plugin is the plugin name from the plugin file

# Define a simple Python function
def print_current_date():
    from datetime import datetime
    print("📅 Current Date:", datetime.now())

# Define the DAG
with DAG(
    dag_id='plugin_demo_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    description='DAG using custom plugin operator with standard operators'
) as dag:

    # Task 1: Custom Operator from Plugin
    greet_task = HelloOperator(
        task_id='greet_task',
        name='Sandeep'
    )

    # Task 2: PythonOperator
    print_date = PythonOperator(
        task_id='print_date_task',
        python_callable=print_current_date
    )

    # Task 3: BashOperator
    run_bash = BashOperator(
        task_id='bash_task',
        bash_command='echo "🖥️ Running Bash Task from DAG"'
    )

    # Define task dependencies
    greet_task >> print_date >> run_bash
