# conftest.py
import pytest
import requests
from apu.utils import login


@pytest.fixture(scope="session")
def auth_token():
    pc_api = login.login()

    # Extract the token from the response
    token = pc_api.token

    if not token:
        raise Exception("Failed to obtain authentication token")

    print(f"\nGenerated auth token: {len(token)}")
    yield token

    # Optional teardown logic can be added here if needed (e.g., logout or token invalidation)
    print("\nSession teardown (e.g., logout)")
