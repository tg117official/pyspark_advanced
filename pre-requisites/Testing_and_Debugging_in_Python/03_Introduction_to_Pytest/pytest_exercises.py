# Prerequisites
# Install pytest:

# pip install pytest

# Exercise 1: Test for equality
# Problem: Write a test to check if a function returns the correct sum of two numbers.
# Relevance: Validates the correctness of mathematical operations in data processing or financial calculations.
def add_numbers(a, b):
    return a + b

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0


# Exercise 2: Test for exceptions
# Problem: Write a test to ensure a function raises a ValueError for invalid inputs.
# Relevance: Ensures functions handle edge cases and invalid inputs gracefully.
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b

def test_divide():
    assert divide(10, 2) == 5.0
    import pytest
    with pytest.raises(ValueError):
        divide(10, 0)


# Exercise 3: Test for lists
# Problem: Write a test to check if a function returns a list of even numbers from a given list.
# Relevance: Validates filtering logic in applications that process collections of data.
def get_even_numbers(numbers):
    return [n for n in numbers if n % 2 == 0]

def test_get_even_numbers():
    assert get_even_numbers([1, 2, 3, 4]) == [2, 4]
    assert get_even_numbers([5, 7, 9]) == []
    assert get_even_numbers([0, -2, -4]) == [0, -2, -4]


# Exercise 4: Test for string manipulation
# Problem: Write a test to validate a function that capitalizes the first letter of every word in a string.
# Relevance: Ensures text formatting functions work as expected in user-facing applications.
def capitalize_words(sentence):
    return " ".join(word.capitalize() for word in sentence.split())

def test_capitalize_words():
    assert capitalize_words("hello world") == "Hello World"
    assert capitalize_words("pytest is great") == "Pytest Is Great"


# Exercise 5: Test for dictionary manipulation
# Problem: Write a test for a function that increments the values in a dictionary by a given amount.
# Relevance: Ensures correct transformations of key-value data structures in ETL pipelines.
def increment_dict_values(d, increment):
    return {k: v + increment for k, v in d.items()}

def test_increment_dict_values():
    assert increment_dict_values({"a": 1, "b": 2}, 1) == {"a": 2, "b": 3}
    assert increment_dict_values({"x": 0, "y": -1}, 5) == {"x": 5, "y": 4}


#################################### INTERMEDIATE ########################################

import pytest
from unittest.mock import Mock, patch

# Exercise 1: Test for parameterized inputs
# Problem: Test a function with multiple inputs and expected outputs using pytest's parameterization.
# Relevance: Ensures functions behave correctly for a variety of inputs, a common QA practice.
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("radar", True),
        ("hello", False),
        ("A man a plan a canal Panama", True),
        ("", True),
        ("12321", True),
    ],
)
def test_is_palindrome(input_str, expected):
    assert is_palindrome(input_str) == expected


# Exercise 2: Test for file reading and writing
# Problem: Write tests for a function that writes and reads data from a file.
# Relevance: Validates file-handling functions, ensuring data persistence works correctly.
def write_and_read_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)
    with open(file_path, "r") as f:
        return f.read()

def test_write_and_read_file(tmp_path):
    file_path = tmp_path / "test.txt"
    data = "Hello, World!"
    result = write_and_read_file(file_path, data)
    assert result == data


# Exercise 3: Mocking external API calls
# Problem: Test a function that fetches data from an API without making actual network requests.
# Relevance: Ensures the function behaves as expected while avoiding reliance on external systems.
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Failed to fetch data")

@patch("requests.get")
def test_fetch_data_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"key": "value"}
    result = fetch_data("https://example.com")
    assert result == {"key": "value"}

@patch("requests.get")
def test_fetch_data_failure(mock_get):
    mock_get.return_value.status_code = 404
    with pytest.raises(ValueError):
        fetch_data("https://example.com")


# Exercise 4: Test for handling missing dictionary keys
# Problem: Write tests for a function that safely retrieves values from a dictionary.
# Relevance: Validates edge-case handling for data lookups, crucial in data processing.
def get_dict_value(data, key, default=None):
    return data.get(key, default)

def test_get_dict_value():
    data = {"name": "Alice", "age": 30}
    assert get_dict_value(data, "name") == "Alice"
    assert get_dict_value(data, "address", "Unknown") == "Unknown"
    assert get_dict_value(data, "age") == 30


# Exercise 5: Integration test with dependency injection
# Problem: Test a function that processes data using a service, using dependency injection to mock the service.
# Relevance: Validates components in isolation while simulating interactions with external dependencies.
class ExternalService:
    def fetch_data(self):
        raise NotImplementedError("This should be mocked")

class DataProcessor:
    def __init__(self, service):
        self.service = service

    def process(self):
        data = self.service.fetch_data()
        return [item.upper() for item in data]

def test_data_processor():
    mock_service = Mock()
    mock_service.fetch_data.return_value = ["hello", "world"]
    processor = DataProcessor(mock_service)
    result = processor.process()
    assert result == ["HELLO", "WORLD"]
    mock_service.fetch_data.assert_called_once()


############################# ADVANCED #############################################

import pytest
from unittest.mock import Mock, patch
import os
import json


# Exercise 1: Custom pytest fixture
# Problem: Write a test for a database connection using a custom pytest fixture.
# Relevance: Demonstrates how to manage reusable setup and teardown logic using fixtures.
@pytest.fixture
def mock_db_connection():
    class MockDB:
        def __init__(self):
            self.connected = False

        def connect(self):
            self.connected = True

        def disconnect(self):
            self.connected = False

        def execute_query(self, query):
            if not self.connected:
                raise ConnectionError("Database not connected")
            return f"Executed: {query}"

    db = MockDB()
    db.connect()
    yield db
    db.disconnect()

def test_mock_db_connection(mock_db_connection):
    db = mock_db_connection
    assert db.connected is True
    assert db.execute_query("SELECT * FROM users") == "Executed: SELECT * FROM users"
    db.disconnect()
    assert db.connected is False


# Exercise 2: Snapshot testing with JSON files
# Problem: Test if a function's output matches a pre-saved JSON snapshot.
# Relevance: Ensures data transformations or API responses remain consistent over time.
def transform_data(data):
    return {k: v.upper() if isinstance(v, str) else v for k, v in data.items()}

@pytest.fixture
def snapshot_path(tmp_path):
    path = tmp_path / "snapshot.json"
    snapshot = {"name": "ALICE", "age": 30}
    with open(path, "w") as f:
        json.dump(snapshot, f)
    return path

def test_transform_data(snapshot_path):
    with open(snapshot_path, "r") as f:
        expected_snapshot = json.load(f)

    result = transform_data({"name": "alice", "age": 30})
    assert result == expected_snapshot


# Exercise 3: Testing asynchronous code
# Problem: Write a test for an async function that fetches data from an API.
# Relevance: Ensures asynchronous functions are tested properly, critical for modern web applications.
import asyncio

async def async_api_call():
    await asyncio.sleep(1)  # Simulate delay
    return {"status": "success"}

@pytest.mark.asyncio
async def test_async_api_call():
    result = await async_api_call()
    assert result == {"status": "success"}


# Exercise 4: Parametrized testing with dependencies
# Problem: Test a service that depends on an external API with multiple scenarios.
# Relevance: Ensures integration points with external systems handle various inputs and responses.
class ExternalService:
    def get_data(self, endpoint):
        raise NotImplementedError("This should be mocked")

@pytest.mark.parametrize(
    "endpoint,response",
    [
        ("/users", [{"id": 1, "name": "Alice"}]),
        ("/posts", [{"id": 101, "title": "Test Post"}]),
    ],
)
@patch.object(ExternalService, "get_data")
def test_external_service(mock_get_data, endpoint, response):
    mock_get_data.return_value = response
    service = ExternalService()
    result = service.get_data(endpoint)
    assert result == response
    mock_get_data.assert_called_once_with(endpoint)


# Exercise 5: End-to-end testing with temporary files and directories
# Problem: Test a mini ETL pipeline that reads data, processes it, and writes output to a file.
# Relevance: Validates the full workflow of data pipelines in an isolated testing environment.
def read_data(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f]

def process_data(data):
    return [line.upper() for line in data]

def write_data(output_path, data):
    with open(output_path, "w") as f:
        f.write("\n".join(data))

def test_etl_pipeline(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    # Create input file
    input_data = ["hello", "world"]
    with open(input_file, "w") as f:
        f.write("\n".join(input_data))

    # Perform ETL steps
    raw_data = read_data(input_file)
    processed_data = process_data(raw_data)
    write_data(output_file, processed_data)

    # Validate output
    with open(output_file, "r") as f:
        output_data = f.read().splitlines()

    assert output_data == ["HELLO", "WORLD"]

