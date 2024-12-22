from airflow import DAG
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator, EmrTerminateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr import EmrJobFlowSensor
from datetime import datetime, timedelta

# Default DAG Arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# EMR Cluster Configuration
JOB_FLOW_OVERRIDES = {
    "Name": "Airflow-EMR-Cluster",
    "ReleaseLabel": "emr-7.0.0",
    "Applications": [{"Name": "Hadoop"}, {"Name": "Spark"}],
    "Instances": {
        "Ec2SubnetId": "subnet-036aa451a22f8a46c",  # Your Subnet
        "Ec2KeyName": "my_key_ec2",  # Replace with your EC2 Key Pair name
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
        "EmrManagedMasterSecurityGroup": "sg-03d1d92a4d4290b9f",  # Master Security Group
        "EmrManagedSlaveSecurityGroup": "sg-0e44780606950a879",   # Slave Security Group
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
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",  # EC2 Instance Profile
    "ServiceRole": "EMR_DefaultRole",      # EMR Service Role
    "LogUri": "s3://aws-logs-146334643284-us-east-1/elasticmapreduce",  # Logs Location
}

# Define the DAG
with DAG(
    "emr_cluster_start_dag",
    default_args=default_args,
    description="Start EMR Cluster with Airflow DAG",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Create EMR Cluster
    create_emr_cluster = EmrCreateJobFlowOperator(
        task_id="create_emr_cluster",
        aws_conn_id="aws_default",  # AWS connection configured in Airflow
        job_flow_overrides=JOB_FLOW_OVERRIDES,
        region_name="us-east-1",  # Replace with your AWS region
    )

    # Task 2: Wait for EMR Cluster to be Ready
    wait_for_emr_cluster = EmrJobFlowSensor(
        task_id="wait_for_emr_cluster",
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
        aws_conn_id="aws_default",
        timeout=3600,  # Timeout in seconds
    )

    # # Task 3: Terminate EMR Cluster (Optional, Replace if Job Steps are added)
    # terminate_emr_cluster = EmrTerminateJobFlowOperator(
    #     task_id="terminate_emr_cluster",
    #     job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    #     aws_conn_id="aws_default",
    # )

    # Task Dependencies
    create_emr_cluster >> wait_for_emr_cluster
