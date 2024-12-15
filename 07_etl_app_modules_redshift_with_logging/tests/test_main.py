import os
import sys

import pytest
from unittest.mock import Mock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.main import main

@patch("src.main.clean_data")
@patch("src.main.write_to_redshift")
@patch("src.main.SparkSession")
def test_main(mock_spark_session, mock_write_to_redshift, mock_clean_data):
    # Mock SparkSession
    mock_spark = Mock()
    mock_spark_session.builder.appName.return_value = mock_spark_session.builder
    mock_spark_session.builder.master.return_value = mock_spark_session.builder
    mock_spark_session.builder.config.return_value = mock_spark_session.builder
    mock_spark_session.builder.getOrCreate.return_value = mock_spark

    # Run the main function
    main()

    # Assertions
    mock_clean_data.assert_called_once()
    mock_write_to_redshift.assert_called_once()
    mock_spark_session.builder.appName.assert_called_once()
