# This test module uses `unittest.mock` to intercept the `requests` calls, allowing you to validate the client's payload generation and error-handling logic without requiring a live Cortex Cloud tenant or exposing real API keys.

import pytest
import os
from unittest.mock import patch, MagicMock
from apu.cortex.core import CortexCloud, Sort, SearchRequestData


@pytest.fixture
def mock_env_vars():
    """Fixture to inject fake credentials into the environment."""
    os.environ["CORTEX_API_BASE_URL"] = "https://api-test.cortex.example.com"
    os.environ["CORTEX_API_KEY_ID"] = "123"
    os.environ["CORTEX_API_KEY"] = "fake_secret_key"
    yield
    # Cleanup
    del os.environ["CORTEX_API_BASE_URL"]
    del os.environ["CORTEX_API_KEY_ID"]
    del os.environ["CORTEX_API_KEY"]


@pytest.fixture
def client(mock_env_vars):  # pytest: disable=unused-argument
    """Fixture to initialize the client with the mocked environment."""
    return CortexCloud(config_file="dummy.env")


@patch("cortex_client.requests.post")
def test_search_cases_success(mock_post, client):
    """Test that search_cases formats the payload correctly and parses a 200 OK."""
    # Mock the API response
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "reply": {
            "total_count": 1,
            "issues": [{"issue_id": "1001", "name": "Exposed S3 Bucket"}],
        }
    }
    mock_post.return_value = mock_response

    # Execute the method
    req_data = SearchRequestData(
        search_from=0, search_to=10, sort=Sort(field="creation_time", keyword="desc")
    )
    result = client.search_cases(req_data)

    # Assertions
    assert result["total_count"] == 1
    assert result["issues"]["name"] == "Exposed S3 Bucket"

    # Verify the payload structure matched Cortex API requirements
    mock_post.assert_called_once()
    called_kwargs = mock_post.call_args.kwargs
    assert called_kwargs["json"]["request_data"]["search_to"] == 10
    assert called_kwargs["json"]["request_data"]["sort"]["field"] == "creation_time"


@patch("cortex_client.requests.post")
def test_raise_on_error_cortex_specific(mock_post, client):
    """Test that the client catches internal Cortex JSON errors (e.g. err_code != 200)."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None  # HTTP 200 OK
    # But the Cortex payload contains an application-level error
    mock_response.json.return_value = {
        "reply": {
            "err_code": 500,
            "err_msg": "An unexpected behavior occurred by Cortex Pubic API",
            "err_extra": "Missing required param: `request_data`",
        }
    }
    mock_post.return_value = mock_response

    req_data = SearchRequestData()

    with pytest.raises(Exception) as exc_info:
        client.search_cases(req_data)

    assert "Cortex API Error [5]" in str(exc_info.value)
    assert "Missing required param" in str(exc_info.value)
