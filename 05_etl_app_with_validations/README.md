# Simple ETL App

This is a modularized ETL application built using PySpark.

## Structure

- `src/`: Contains the ETL logic.
- `config/`: Configuration files.
- `data/`: Input and output data.
- `main.py`: Entry point for the application.
- `requirements.txt`: Python dependencies.

## Usage

1. Install dependencies:


2. Run the application:


## ETL Workflow

1. **Clean Data**:
Removes nulls and duplicates.

2. **Transformations**:
Applies business logic transformations.

3. **Aggregations**:
Calculates summaries like total sales.

## Configuration

Update the file paths in `config/config.yaml` to match your environment.
