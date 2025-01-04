import unittest
from unittest.mock import patch, Mock
import os
import requests
import json

# Exercise 1: Testing asynchronous functions
# Problem: Write a test case for an asynchronous function that fetches data from an API.
# Relevance: Validates functionality in asynchronous code, critical for modern web applications.
import asyncio

async def async_fetch_data(url):
    await asyncio.sleep(1)  # Simulates delay
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Failed to fetch data")

class TestAsyncFunction(unittest.IsolatedAsyncioTestCase):
    @patch("requests.get")
    async def test_async_fetch_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "value"}
        result = await async_fetch_data("https://example.com")
        self.assertEqual(result, {"data": "value"})

# Exercise 2: Testing a decorator
# Problem: Write a test case for a function that uses a decorator to log its calls.
# Relevance: Ensures decorators modify functions correctly without breaking functionality.
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    return a + b

class TestDecorator(unittest.TestCase):
    @patch("builtins.print")
    def test_logger_decorator(self, mock_print):
        result = add(2, 3)
        self.assertEqual(result, 5)
        mock_print.assert_called_with("Calling add with args=(2, 3), kwargs={}.")

# Exercise 3: Testing dynamic configurations with environment variables
# Problem: Test a function that retrieves configurations from environment variables.
# Relevance: Ensures dynamic configurations, like database URLs, are handled correctly.
def get_config():
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise EnvironmentError("DB_URL is not set")
    return db_url

class TestConfig(unittest.TestCase):
    @patch.dict(os.environ, {"DB_URL": "postgres://user:pass@localhost/db"})
    def test_get_config_success(self):
        self.assertEqual(get_config(), "postgres://user:pass@localhost/db")

    @patch.dict(os.environ, {}, clear=True)
    def test_get_config_failure(self):
        with self.assertRaises(EnvironmentError):
            get_config()

# Exercise 4: Testing a complex class with dependency injection
# Problem: Test a class that interacts with an external service using dependency injection.
# Relevance: Validates components in isolation, avoiding reliance on external dependencies.
class ExternalService:
    def fetch_data(self):
        raise NotImplementedError("This should be mocked")

class DataProcessor:
    def __init__(self, service):
        self.service = service

    def process(self):
        data = self.service.fetch_data()
        return [d.upper() for d in data]

class TestDataProcessor(unittest.TestCase):
    def test_process(self):
        mock_service = Mock()
        mock_service.fetch_data.return_value = ["hello", "world"]
        processor = DataProcessor(mock_service)
        result = processor.process()
        self.assertEqual(result, ["HELLO", "WORLD"])
        mock_service.fetch_data.assert_called_once()

# Exercise 5: Snapshot testing with JSON data
# Problem: Test a function that transforms JSON data against a snapshot.
# Relevance: Ensures consistent transformations in data pipelines or APIs.
def transform_json(data):
    transformed = {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}
    return transformed

class TestSnapshot(unittest.TestCase):
    def setUp(self):
        self.snapshot_path = "snapshot.json"
        if not os.path.exists(self.snapshot_path):
            with open(self.snapshot_path, "w") as f:
                json.dump({"name": "JOHN", "age": 30}, f)

    def tearDown(self):
        if os.path.exists(self.snapshot_path):
            os.remove(self.snapshot_path)

    def test_transform_json(self):
        with open(self.snapshot_path, "r") as f:
            snapshot = json.load(f)
        result = transform_json({"name": "john", "age": 30})
        self.assertEqual(result, snapshot)

# Run all the test cases
if __name__ == "__main__":
    unittest.main()
