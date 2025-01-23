#!/bin/bash

# Check if environment argument is provided
if [ -z "$1" ]; then
    echo "Error: No environment specified."
    echo "Usage: ./run_pipeline.sh <env>"
    echo "Example: ./run_pipeline.sh dev"
    exit 1
fi

ENV=$1

# Validate environment
if [[ "$ENV" != "dev" && "$ENV" != "prod" ]]; then
    echo "Error: Invalid environment specified. Choose 'dev' or 'prod'."
    exit 1
fi

# Define application and configuration paths
APP_NAME="ETL Pipeline"
APP_ENTRY="main.py"
CONFIG_PATH="config/config.yaml"
LOGGING_PATH="config/logging_config.yaml"
MASTER="yarn"  # Use 'local[*]' for local mode, 'yarn' for EMR
DEPLOY_MODE="cluster"

# Construct spark-submit command
spark-submit \
  --master $MASTER \
  --deploy-mode $DEPLOY_MODE \
  --name "$APP_NAME - $ENV" \
  --files "$CONFIG_PATH,$LOGGING_PATH" \
  $APP_ENTRY \
  --env $ENV
