import pytest
from unittest.mock import patch
import os
import requests

# Exercise 1: Test for multiple cases with parameterization
# Problem: Write a test case to verify a function that checks if a string is a palindrome.
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

@pytest.mark.parametrize("input_str, expected", [
    ("radar", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("", True),
])
def test_palindromes(input_str, expected):
    assert is_palindrome(input_str) == expected

# Exercise 2: Test setup and teardown
# Problem: Write a test case for a calculator class with setup and teardown methods.
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(2, 3) == 5

def test_multiply(calculator):
    assert calculator.multiply(2, 3) == 6

# Exercise 3: Mocking external API calls
# Problem: Write a test case to mock an API call and verify behavior without actual network requests.
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
    assert fetch_data("https://example.com") == {"key": "value"}

@patch("requests.get")
def test_fetch_data_failure(mock_get):
    mock_get.return_value.status_code = 404
    with pytest.raises(ValueError):
        fetch_data("https://example.com")

# Exercise 4: Testing file operations
# Problem: Write a test case for a function that writes and reads data from a file.
def write_and_read_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)
    with open(file_path, "r") as f:
        return f.read()

@pytest.fixture
def test_file():
    file_path = "test_file.txt"
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

def test_write_and_read(test_file):
    data = "Hello, World!"
    result = write_and_read_file(test_file, data)
    assert result == data

# Exercise 5: Integration test for a mini application
# Problem: Test an end-to-end workflow of a shopping cart application.
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})

    def get_total(self):
        return sum(item["price"] for item in self.items)

@pytest.fixture
def shopping_cart():
    return ShoppingCart()

def test_add_item(shopping_cart):
    shopping_cart.add_item("Apple", 1.5)
    shopping_cart.add_item("Banana", 2.0)
    assert len(shopping_cart.items) == 2

def test_get_total(shopping_cart):
    shopping_cart.add_item("Apple", 1.5)
    shopping_cart.add_item("Banana", 2.0)
    assert pytest.approx(shopping_cart.get_total(), 0.1) == 3.5

# To run all the test cases, execute the following command in the terminal:
# pytest <script_name>.py
