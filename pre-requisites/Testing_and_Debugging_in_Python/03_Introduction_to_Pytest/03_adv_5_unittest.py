import pytest
from unittest.mock import patch, Mock
import os
import requests
import json
import asyncio

# Exercise 1: Testing asynchronous functions
# Problem: Write a test case for an asynchronous function that fetches data from an API.
async def async_fetch_data(url):
    await asyncio.sleep(1)  # Simulates delay
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Failed to fetch data")

@patch("requests.get")
@pytest.mark.asyncio
async def test_async_fetch_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "value"}
    result = await async_fetch_data("https://example.com")
    assert result == {"data": "value"}

# Exercise 2: Testing a decorator
# Problem: Write a test case for a function that uses a decorator to log its calls.
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

@patch("builtins.print")
def test_logger_decorator(mock_print):
    result = add(2, 3)
    assert result == 5
    mock_print.assert_called_with("Calling add with args=(2, 3), kwargs={}.")

# Exercise 3: Testing dynamic configurations with environment variables
# Problem: Test a function that retrieves configurations from environment variables.
def get_config():
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise EnvironmentError("DB_URL is not set")
    return db_url

@patch.dict(os.environ, {"DB_URL": "postgres://user:pass@localhost/db"})
def test_get_config_success():
    assert get_config() == "postgres://user:pass@localhost/db"

@patch.dict(os.environ, {}, clear=True)
def test_get_config_failure():
    with pytest.raises(EnvironmentError):
        get_config()

# Exercise 4: Testing a complex class with dependency injection
# Problem: Test a class that interacts with an external service using dependency injection.
class ExternalService:
    def fetch_data(self):
        raise NotImplementedError("This should be mocked")

class DataProcessor:
    def __init__(self, service):
        self.service = service

    def process(self):
        data = self.service.fetch_data()
        return [d.upper() for d in data]

def test_data_processor():
    mock_service = Mock()
    mock_service.fetch_data.return_value = ["hello", "world"]
    processor = DataProcessor(mock_service)
    result = processor.process()
    assert result == ["HELLO", "WORLD"]
    mock_service.fetch_data.assert_called_once()

# Exercise 5: Snapshot testing with JSON data
# Problem: Test a function that transforms JSON data against a snapshot.
def transform_json(data):
    transformed = {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}
    return transformed

@pytest.fixture
def snapshot_file():
    snapshot_path = "snapshot.json"
    if not os.path.exists(snapshot_path):
        with open(snapshot_path, "w") as f:
            json.dump({"name": "JOHN", "age": 30}, f)
    yield snapshot_path
    if os.path.exists(snapshot_path):
        os.remove(snapshot_path)

def test_transform_json(snapshot_file):
    with open(snapshot_file, "r") as f:
        snapshot = json.load(f)
    result = transform_json({"name": "john", "age": 30})
    assert result == snapshot

# To run all the test cases, execute the following command in the terminal:
# pytest <script_name>.py
