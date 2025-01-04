import unittest

# Exercise 1: Test for equality
# Problem: Write a test case to check if a function returns the correct sum of two numbers.
# Relevance: Validating the correctness of mathematical operations is essential in numerical or financial applications.
def add_numbers(a, b):
    return a + b

class TestAddition(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)

# Exercise 2: Test for exceptions
# Problem: Write a test case to check if a function raises a `ValueError` for invalid inputs.
# Relevance: Ensures functions handle edge cases and invalid inputs gracefully.
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b

class TestDivision(unittest.TestCase):
    def test_division(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

# Exercise 3: Test for list contents
# Problem: Write a test case to check if a function returns a list of even numbers.
# Relevance: Validates correct filtering logic in data processing functions.
def get_even_numbers(numbers):
    return [n for n in numbers if n % 2 == 0]

class TestEvenNumbers(unittest.TestCase):
    def test_get_even_numbers(self):
        self.assertEqual(get_even_numbers([1, 2, 3, 4]), [2, 4])
        self.assertEqual(get_even_numbers([5, 7, 9]), [])
        self.assertEqual(get_even_numbers([0, -2, -4]), [0, -2, -4])

# Exercise 4: Test for string output
# Problem: Write a test case to validate a function that capitalizes words in a string.
# Relevance: Common in applications requiring text formatting, such as titles or labels.
def capitalize_words(sentence):
    return " ".join(word.capitalize() for word in sentence.split())

class TestStringCapitalization(unittest.TestCase):
    def test_capitalize_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")
        self.assertEqual(capitalize_words("python unittest"), "Python Unittest")

# Exercise 5: Test for dictionary manipulation
# Problem: Write a test case to validate a function that increments values in a dictionary by a given amount.
# Relevance: Ensures correctness in data transformations often required in ETL processes.
def increment_dict_values(d, increment):
    return {k: v + increment for k, v in d.items()}

class TestIncrementDict(unittest.TestCase):
    def test_increment_dict_values(self):
        self.assertEqual(
            increment_dict_values({"a": 1, "b": 2}, 1), {"a": 2, "b": 3}
        )
        self.assertEqual(
            increment_dict_values({"x": 0, "y": -1}, 5), {"x": 5, "y": 4}
        )

# Run all the test cases
if __name__ == "__main__":
    unittest.main()
