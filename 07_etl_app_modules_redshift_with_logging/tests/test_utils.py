import os
import sys

import pytest
from unittest.mock import mock_open, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from src.utils import read_config

def test_read_config():
    mock_config = """
    environments:
      dev:
        paths:
          s3_input_path: "mock_path"
    """
    with patch("builtins.open", mock_open(read_data=mock_config)):
        config = read_config()
        assert config["environments"]["dev"]["paths"]["s3_input_path"] == "mock_path"
