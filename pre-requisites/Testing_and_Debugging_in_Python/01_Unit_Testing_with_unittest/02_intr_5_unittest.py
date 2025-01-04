import unittest

# Exercise 1: Test for multiple cases with parameterization
# Problem: Write a test case to verify a function that checks if a string is a palindrome.
# Relevance: Ensures multiple inputs are tested comprehensively, a common practice in QA and software validation.
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

class TestPalindrome(unittest.TestCase):
    def test_palindromes(self):
        cases = [
            ("radar", True),
            ("hello", False),
            ("A man a plan a canal Panama", True),
            ("", True),
        ]
        for input_str, expected in cases:
            with self.subTest(input_str=input_str):
                self.assertEqual(is_palindrome(input_str), expected)

# Exercise 2: Test setup and teardown
# Problem: Write a test case for a calculator class with setup and teardown methods.
# Relevance: Demonstrates reusable setup/cleanup logic for objects or data shared across multiple tests.
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        print("Setup complete.")

    def tearDown(self):
        print("Teardown complete.")

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(2, 3), 6)

# Exercise 3: Mocking external API calls
# Problem: Write a test case to mock an API call and verify behavior without actual network requests.
# Relevance: Essential for testing functions dependent on external services without incurring network overhead.
import requests
from unittest.mock import patch

def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Failed to fetch data")

class TestAPI(unittest.TestCase):
    @patch("requests.get")
    def test_fetch_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "value"}
        self.assertEqual(fetch_data("https://example.com"), {"key": "value"})

    @patch("requests.get")
    def test_fetch_data_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        with self.assertRaises(ValueError):
            fetch_data("https://example.com")

# Exercise 4: Testing file operations
# Problem: Write a test case for a function that writes and reads data from a file.
# Relevance: Validates functionality that interacts with files, ensuring correctness in storage and retrieval.
def write_and_read_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)
    with open(file_path, "r") as f:
        return f.read()

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.file_path = "test_file.txt"

    def tearDown(self):
        import os
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_write_and_read(self):
        data = "Hello, World!"
        result = write_and_read_file(self.file_path, data)
        self.assertEqual(result, data)

# Exercise 5: Integration test for a mini application
# Problem: Test an end-to-end workflow of a shopping cart application.
# Relevance: Ensures the integration of components in a system functions as expected.
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})

    def get_total(self):
        return sum(item["price"] for item in self.items)

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("Apple", 1.5)
        self.cart.add_item("Banana", 2.0)
        self.assertEqual(len(self.cart.items), 2)

    def test_get_total(self):
        self.cart.add_item("Apple", 1.5)
        self.cart.add_item("Banana", 2.0)
        self.assertAlmostEqual(self.cart.get_total(), 3.5, places=1)

# Run all the test cases
if __name__ == "__main__":
    unittest.main()
