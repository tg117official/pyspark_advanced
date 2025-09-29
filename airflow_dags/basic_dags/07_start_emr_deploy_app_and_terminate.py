from airflow import DAG
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator, EmrTerminateJobFlowOperator, EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr import EmrJobFlowSensor, EmrStepSensor
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'emr_spark_submit_terminate_on_any_2',
    default_args=default_args,
    description='A DAG to start EMR, submit a Spark job, and terminate the cluster regardless of step outcome',
    schedule_interval=None,
)

# EMR Cluster Configuration
JOB_FLOW_OVERRIDES = {
    "Name": "Airflow-EMR-Cluster",
    "ReleaseLabel": "emr-7.8.0",
    "Applications": [{"Name": "Hadoop"}, {"Name": "Spark"}],
    "Instances": {
        "Ec2SubnetId": "subnet-036aa451a22f8a46c",  # Your Subnet
        "Ec2KeyName": "your-ec2-key",  # Replace with your EC2 Key Pair name
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
                "InstanceCount": 1,
            },
        ],
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",  # EC2 Instance Profile
    "ServiceRole": "EMR_DefaultRole",      # EMR Service Role
    "LogUri": "s3://aws-logs-146334643284-us-east-1/elasticmapreduce",  # Logs Location
}


# Spark step configuration
SPARK_STEPS = [
    {
        'Name': 'Run Spark job',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--master', 'yarn',
                '--deploy-mode', 'cluster',
                '--archives', 's3://emr-serverless-tg117/scripts/pyspark_venv.tar.gz#environment',
                '--py-files', 's3://emr-serverless-tg117/scripts/project_new.zip',
                '--conf', 'spark.yarn.appMasterEnv.PYSPARK_PYTHON=./environment/bin/python',
                '--conf', 'spark.executorEnv.PYSPARK_PYTHON=./environment/bin/python',
                's3://emr-serverless-tg117/scripts/run_pipeline.py',
            ],
        },
    }
]

# Task 1: Create EMR cluster
create_emr_cluster = EmrCreateJobFlowOperator(
    task_id='create_emr_cluster',
    job_flow_overrides=JOB_FLOW_OVERRIDES,
    aws_conn_id='aws_default',
    dag=dag,
)

# Task 2: Wait for the cluster to reach the WAITING state
wait_for_emr_cluster = EmrJobFlowSensor(
    task_id='wait_for_emr_cluster',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    aws_conn_id='aws_default',
    target_states=['WAITING'],  # Wait for the cluster to reach WAITING
    poke_interval=60,  # Check every 60 seconds
    timeout=600,  # Timeout after 10 minutes
    dag=dag,
)

# Task 3: Add Spark step
add_spark_step = EmrAddStepsOperator(
    task_id='add_spark_step',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    steps=SPARK_STEPS,
    aws_conn_id='aws_default',
    dag=dag,
)

# Task 4: Monitor Spark step
monitor_spark_step = EmrStepSensor(
    task_id='monitor_spark_step',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    step_id="{{ task_instance.xcom_pull(task_ids='add_spark_step', key='return_value')[0] }}",
    aws_conn_id='aws_default',
    dag=dag,
)

# Task 5: Terminate EMR cluster
terminate_emr_cluster = EmrTerminateJobFlowOperator(
    task_id='terminate_emr_cluster',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    aws_conn_id='aws_default',
    trigger_rule=TriggerRule.ALL_DONE,  # Run this task regardless of upstream task success or failure
    dag=dag,
)

# Set task dependencies
create_emr_cluster >> wait_for_emr_cluster >> add_spark_step >> monitor_spark_step >> terminate_emr_cluster
