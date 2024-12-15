import boto3
import yaml
import time
import sys
import os

os.environ['ENV']='dev'

def read_config(config_path=r"C:\Users\Sandeep\PycharmProjects\pyspark_advanced\07_etl_app_modules_redshift_with_logging\config\config.yaml", environment="dev"):
    """
    Reads the configuration file and fetches environment-specific configurations.
    """
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config["environments"][environment]

def submit_spark_job(config, cluster_id):
    """
    Submits a Spark job to an EMR cluster using Boto3 and the provided configurations.
    """
    # Prepare the Spark submit step based on the configuration
    spark_step = {
        'Name': f"Run {config['spark']['app_name']}",
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', config['spark']['deploy_mode'],
                '--master', config['spark']['master'],
                '--conf', f"spark.executor.memory={config['spark']['executor_memory']}",
                '--conf', f"spark.executor.cores={config['spark']['executor_cores']}",
                '--conf', f"spark.sql.shuffle.partitions={config['spark']['shuffle_partitions']}",
                '--conf', f"spark.dynamicAllocation.enabled={str(config['spark']['dynamic_allocation_enabled']).lower()}",
                '--conf', f"spark.dynamicAllocation.minExecutors={config['spark']['dynamic_allocation_min_executors']}",
                '--conf', f"spark.dynamicAllocation.maxExecutors={config['spark']['dynamic_allocation_max_executors']}",
                config['paths']['s3_app_path']  # Replace with actual application path
            ]
        }
    }

    # Initialize Boto3 EMR client
    client = boto3.client('emr', region_name='us-east-1')  # Update region as necessary

    # Submit the job step
    response = client.add_job_flow_steps(
        JobFlowId=cluster_id,
        Steps=[spark_step]
    )

    # Extract step ID and print status
    step_id = response['StepIds'][0]
    print(f"Submitted job with Step ID: {step_id}")

    # Monitor the job status
    monitor_step_status(client, cluster_id, step_id)

def monitor_step_status(client, cluster_id, step_id):
    """
    Monitors the status of the submitted step until it completes.
    """
    while True:
        response = client.describe_step(ClusterId=cluster_id, StepId=step_id)
        status = response['Step']['Status']['State']
        print(f"Step status: {status}")
        if status in ['COMPLETED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(30)
    print(f"Final step status: {status}")

if __name__ == "__main__":
    # Read command-line arguments for environment and cluster ID
    if len(sys.argv) < 3:
        print("Usage: python deploy_app_to_emr.py <environment> <cluster_id>")
        sys.exit(1)

    environment = sys.argv[1]
    cluster_id = sys.argv[2]

    # Read the configuration for the specified environment
    config = read_config(environment=environment)

    # Submit the Spark job
    submit_spark_job(config, cluster_id)
