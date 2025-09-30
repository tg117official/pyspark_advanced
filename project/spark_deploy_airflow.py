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
    'spark_deploy_airflow',
    default_args=default_args,
    description='A DAG to start EMR, submit a Spark job, and terminate the cluster regardless of step outcome',
    schedule_interval=None,
)

# EMR Cluster Configuration
JOB_FLOW_OVERRIDES = {
    "Name": "Airflow-EMR-Cluster",
    "ReleaseLabel": "emr-7.10.0",
    "Applications": [{"Name": "Hadoop"}, {"Name": "Spark"}],
    "Instances": {
        "Ec2SubnetId": "subnet-00bba6aca2d23b553",  # Your Subnet
        "Ec2KeyName": "us-east-1-demo-key-pair",  # Replace with your EC2 Key Pair name
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
        "EmrManagedMasterSecurityGroup": "sg-0704ee3e3b83d49b4",  # Master Security Group
        "EmrManagedSlaveSecurityGroup": "sg-0d71631fd8de29fc6",   # Slave Security Group
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
    "JobFlowRole": "AmazonEMR-InstanceProfile-20250921T123013",  # EC2 Instance Profile
    "ServiceRole": "AmazonEMR-ServiceRole-20250921T123033",      # EMR Service Role
    "LogUri": "s3://aws-emr-logs111777/emrlogs/ ",  # Logs Location
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
                '--archives', 's3://emr-exercises-tg117/project/pyspark_venv.tar.gz#environment',
                '--py-files', 's3://emr-exercises-tg117/project/project.zip',
                '--conf', 'spark.yarn.appMasterEnv.PYSPARK_PYTHON=./environment/bin/python',
                '--conf', 'spark.executorEnv.PYSPARK_PYTHON=./environment/bin/python',
                's3://emr-exercises-tg117/project/main.py',
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

# Task 1: EmrCreateJobFlowOperator (Create EMR Cluster)
# task_id → Unique name for the task (create_emr_cluster).
# job_flow_overrides → Dictionary with EMR cluster configuration (like instance type, count, release label, applications, etc.).
# aws_conn_id → AWS connection configured in Airflow (aws_default).
# dag → The DAG object this task belongs to.

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

# Task 2: EmrJobFlowSensor (Wait for Cluster)
# task_id → Unique name for the task (wait_for_emr_cluster).
# job_flow_id → Pulls cluster ID from XCom (output of Task 1).
# aws_conn_id → AWS connection.
# target_states → List of states to wait for (WAITING means cluster is ready for jobs).
# poke_interval → How often to check status (every 60 seconds).
# timeout → Maximum wait time before failing (600 seconds = 10 minutes).
# dag → The DAG object.

# Task 3: Add Spark step
add_spark_step = EmrAddStepsOperator(
    task_id='add_spark_step',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    steps=SPARK_STEPS,
    aws_conn_id='aws_default',
    dag=dag,
)

# Task 3: EmrAddStepsOperator (Add Spark Step)
# task_id → Unique name (add_spark_step).
# job_flow_id → Cluster ID from Task 1.
# steps → List of steps to add (like Spark job details: JAR/script, arguments, etc.).
# aws_conn_id → AWS connection.
# dag → The DAG object.


# Task 4: Monitor Spark step
monitor_spark_step = EmrStepSensor(
    task_id='monitor_spark_step',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    step_id="{{ task_instance.xcom_pull(task_ids='add_spark_step', key='return_value')[0] }}",
    aws_conn_id='aws_default',
    dag=dag,
)

# Task 4: EmrStepSensor (Monitor Spark Step)
# task_id → Unique name (monitor_spark_step).
# job_flow_id → Cluster ID from Task 1.
# step_id → Step ID pulled from Task 3.
# aws_conn_id → AWS connection.
# dag → The DAG object.

# Task 5: Terminate EMR cluster
terminate_emr_cluster = EmrTerminateJobFlowOperator(
    task_id='terminate_emr_cluster',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
    aws_conn_id='aws_default',
    trigger_rule=TriggerRule.ALL_DONE,  # Run this task regardless of upstream task success or failure
    dag=dag,
)
# Task 5: EmrTerminateJobFlowOperator (Terminate Cluster)
# task_id → Unique name (terminate_emr_cluster).
# job_flow_id → Cluster ID from Task 1.
# aws_conn_id → AWS connection.
# trigger_rule → Defines when this task should run. ALL_DONE means it will run regardless of whether upstream tasks succeed or fail (ensures cluster is always terminated).
# dag → The DAG object.


# Set task dependencies
create_emr_cluster >> wait_for_emr_cluster >> add_spark_step >> monitor_spark_step >> terminate_emr_cluster

















