# Nested module demonstrating relative imports
from .sub_utils import helper_function

def nested_function():
    print("Nested function in nested.py")
    helper_function()

