from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator, EmrTerminateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr import EmrJobFlowSensor
from datetime import datetime, timedelta
import time

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
    's3_to_emr_dag',
    default_args=default_args,
    description='A DAG to wait for files on S3, create an EMR cluster, monitor it, and terminate it',
    schedule_interval=None,
)

# S3 Bucket and Key Prefix
S3_BUCKET_NAME = 'your-s3-bucket-name'
S3_KEY_PREFIX = 'path/to/files/'

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
                "InstanceCount": 2,
            },
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",
    "ServiceRole": "EMR_DefaultRole",
}

# Task 1: Wait for files on S3
wait_for_files = S3KeySensor(
    task_id='wait_for_files_on_s3',
    bucket_name=S3_BUCKET_NAME,
    bucket_key=f'{S3_KEY_PREFIX}*',
    aws_conn_id='aws_default',
    timeout=600,  # Wait up to 10 minutes for the files to arrive
    poke_interval=30,  # Check every 30 seconds
    dag=dag,
)

# Task 2: Create EMR cluster
create_emr_cluster = EmrCreateJobFlowOperator(
    task_id='create_emr_cluster',
    job_flow_overrides=JOB_FLOW_OVERRIDES,
    aws_conn_id='aws_default',
    region_name='us-east-1',
    dag=dag,
)

# Task 3: Monitor EMR cluster for 5 minutes
monitor_emr_cluster = EmrJobFlowSensor(
    task_id='monitor_emr_cluster',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    aws_conn_id='aws_default',
    timeout=300,  # Monitor for up to 5 minutes
    poke_interval=60,  # Check every 1 minute
    dag=dag,
)

# Task 4: Terminate EMR cluster
terminate_emr_cluster = EmrTerminateJobFlowOperator(
    task_id='terminate_emr_cluster',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    aws_conn_id='aws_default',
    dag=dag,
)

# Set task dependencies
wait_for_files >> create_emr_cluster >> monitor_emr_cluster >> terminate_emr_cluster
