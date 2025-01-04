import unittest
from unittest.mock import patch

# Import the functions to be tested
from project_package.utils import utility_function
from project_package.sub_package.nested import nested_function
from project_package.sub_package.sub_utils import helper_function
from r1.standalone_module import standalone_function
from project_package.main import main

class TestProject(unittest.TestCase):

    def test_utility_function(self):
        with patch('builtins.print') as mock_print:
            utility_function()
            mock_print.assert_called_once_with("Utility function in utils.py")

    def test_helper_function(self):
        with patch('builtins.print') as mock_print:
            helper_function()
            mock_print.assert_called_once_with("Helper function in sub_utils.py")

    def test_nested_function(self):
        with patch('project_package.sub_package.sub_utils.helper_function') as mock_helper:
            with patch('builtins.print') as mock_print:
                nested_function()
                mock_print.assert_called_once_with("Nested function in nested.py")
                mock_helper.assert_called_once()

    def test_standalone_function(self):
        with patch('builtins.print') as mock_print:
            standalone_function()
            mock_print.assert_called_once_with("Standalone function in standalone_module.py")

    @patch('project_package.main.utility_function')
    @patch('project_package.main.helper_function')
    @patch('project_package.main.nested_function')
    @patch('project_package.main.external_function')
    @patch('builtins.print')
    def test_main(self, mock_print, mock_external, mock_nested, mock_helper, mock_utility):
        main()
        mock_print.assert_any_call("Running run_pipeline.py")
        mock_utility.assert_called_once()
        mock_helper.assert_called_once()
        mock_nested.assert_called_once()
        mock_external.assert_called_once()

if __name__ == "__main__":
    unittest.main()
