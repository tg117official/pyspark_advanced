import pytest

# Exercise 1: Test for equality
# Problem: Write a test case to check if a function returns the correct sum of two numbers.
# Relevance: Validating the correctness of mathematical operations is essential in numerical or financial applications.
def add_numbers(a, b):
    return a + b


add_numbers(10,5)
def test_addition():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0