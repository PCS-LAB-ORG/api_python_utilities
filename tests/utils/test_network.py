# Using unittest.mock to raise a ConnectionError
from unittest.mock import patch

import requests

from apu.errors import branch_scan


@patch("requests.get")
def test_network_failure(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError
    # ... test how your code handles the error
    branch_scan.branch_scan()
