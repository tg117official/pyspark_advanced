from datetime import datetime
from airflow import DAG
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.sensors.emr import EmrJobFlowSensor

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

# Define EMR Cluster Configuration
JOB_FLOW_OVERRIDES = {
    "Name": "Airflow-EMR-Cluster",
    "ReleaseLabel": "emr-6.10.0",  # Use the appropriate EMR release
    "Applications": [{"Name": "Spark"}, {"Name": "Hadoop"}],
    "Configurations": [],
    "Instances": {
        "InstanceGroups": [
            {
                "Name": "Master node",
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
        "Ec2KeyName": "your-ec2-key",  # Replace with your EC2 key pair name
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
    },
    "VisibleToAllUsers": True,
    "JobFlowRole": "AmazonEMR-InstanceProfile-20241213T162731",  # Ensure this role exists in your AWS account
    "ServiceRole": "AmazonEMR-ServiceRole-20241213T162750",  # Ensure this role exists in your AWS account
}

# Define the DAG
with DAG(
    dag_id="launch_emr_cluster",
    default_args=default_args,
    description="DAG to launch an EMR cluster",
    schedule_interval=None,  # Set to desired schedule interval
    start_date=datetime(2023, 12, 1),
    catchup=False,
    tags=["emr", "aws"],
) as dag:

    # Task to create EMR cluster
    create_emr_cluster = EmrCreateJobFlowOperator(
        task_id="create_emr_cluster",
        job_flow_overrides=JOB_FLOW_OVERRIDES,
        aws_conn_id="aws_default",  # Replace with your AWS connection ID if different
    )

    # Task to wait for the EMR cluster to be ready
    wait_for_emr_cluster = EmrJobFlowSensor(
        task_id="wait_for_emr_cluster",
        job_flow_id=create_emr_cluster.output,
        aws_conn_id="aws_default",  # Replace with your AWS connection ID if different
    )

    # Define task dependencies
    create_emr_cluster >> wait_for_emr_cluster
