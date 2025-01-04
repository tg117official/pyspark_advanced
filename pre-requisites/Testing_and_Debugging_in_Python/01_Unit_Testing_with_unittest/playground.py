import unittest
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