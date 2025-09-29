from airflow.plugins_manager import AirflowPlugin
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

# Custom Operator
class HelloOperator(BaseOperator):
    @apply_defaults
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    def execute(self, context):
        print(f"👋 Hello, {self.name}! This message is from a custom Airflow plugin.")

# Plugin Definition
class HelloPlugin(AirflowPlugin):
    name = "hello_plugin"
    operators = [HelloOperator]
