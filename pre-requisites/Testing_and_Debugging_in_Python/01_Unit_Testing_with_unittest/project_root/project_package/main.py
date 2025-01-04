import sys
import os

# Add the external_module directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))  # Path to run_pipeline.py
external_module_path = os.path.abspath(os.path.join(current_dir, "../external_module"))
sys.path.append(external_module_path)

# Import external_function from external.py
from external import external_function

# Existing imports
from .utils import utility_function
from .sub_package.sub_utils import helper_function
from .sub_package.nested import nested_function

def main() :
    print(current_dir)
    print(external_module_path)
    print("Running run_pipeline.py")
    utility_function()
    helper_function()
    nested_function()
    external_function()  # Call the function from external_module

if __name__ == "__main__" :
    main()
