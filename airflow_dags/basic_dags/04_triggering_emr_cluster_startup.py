from airflow import DAG
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator, EmrTerminateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr import EmrJobFlowSensor
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def print_success():
    print("EMR Cluster Created Successfully")

# Default arguments for the DAG
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
    'emr_cluster_creation',
    default_args=default_args,
    description='A DAG to create and terminate an EMR cluster',
    schedule_interval=None,
)

# EMR cluster configuration
JOB_FLOW_OVERRIDES = {
    "Name": "Airflow-EMR-Cluster",
    "ReleaseLabel": "emr-6.7.0",
    "Applications": [{"Name": "Hadoop"}, {"Name": "Spark"}],
    "Instances": {
        "InstanceGroups": [
            {
                "Name": "Master nodes",
                "Market": "ON_DEMAND",
                "InstanceRole": "MASTER",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 1,
            },
            {
                "Name": "Core nodes",
                "Market": "ON_DEMAND",
                "InstanceRole": "CORE",
                "InstanceType": "m5.xlarge",
                "InstanceCount": 1,
            },
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
    },
    "JobFlowRole": "AmazonEMR-InstanceProfile-20241213T162731",
    "ServiceRole": "AmazonEMR-ServiceRole-20241213T162750",



}

# Task 1: Create EMR cluster
create_emr_cluster = EmrCreateJobFlowOperator(
    task_id='create_emr_cluster',
    job_flow_overrides=JOB_FLOW_OVERRIDES,
    aws_conn_id='aws_default',
    region_name='us-east-1',  # Valid here
    dag=dag,
)

# # Task 2: Monitor EMR cluster
# monitor_emr_cluster = EmrJobFlowSensor(
#     task_id='monitor_emr_cluster',
#     job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
#     aws_conn_id='aws_default',
#     dag=dag,  # No region_name here
# )

# Task 3: Terminate EMR cluster
# terminate_emr_cluster = EmrTerminateJobFlowOperator(
#     task_id='terminate_emr_cluster',
#     job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
#     aws_conn_id='aws_default',  # Removed region_name
#     dag=dag,
# )
# Task 3: Print "Goodbye"
task_2 = PythonOperator(
    task_id='print_goodbye',
    python_callable=print_success,
    dag=dag,
)
# Set task dependencies
create_emr_cluster >> task_2