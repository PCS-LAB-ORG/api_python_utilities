# Cortex Cloud Python Client

This client provides a type-safe, environment-aware wrapper for interacting with the Cortex Cloud APIs. It natively handles authentication, environment variable parsing (via `dotenv`), and Cortex-specific error handling.

## How to Extend the Client

Because the Cortex Cloud platform contains hundreds of APIs across Core, Application Security (AppSec), Cloud Workload Protection (CWP), and Data Security, you will likely need to add endpoints specific to your operational logic [1-3].

### Step 1: Define a Type-Safe Dataclass (Optional but Recommended)
For endpoints requiring a complex JSON body, create a `dataclass` to ensure type safety. 
```python
from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class AssetFilterData:
    search_from: int = 0
    search_to: int = 100
    on_demand_fields: Optional[List[str]] = None
Step 2: Create the API Method
Add a new method to the CortexCloudClient class. Use asdict() to convert your dataclass into the dictionary structure Cortex requires, ensuring you nest it under the "request_data" key if the API demands it
.
Use the internal _make_request(method, endpoint, payload) method. It automatically appends your authentication headers and runs the response through the raise_on_error() validator
.
    def get_assets(self, filter_data: AssetFilterData):
        """Retrieve detailed information about assets."""
        # Clean None values from the dictionary before sending
        payload = {"request_data": {k: v for k, v in asdict(filter_data).items() if v is not None}}
        data = self._make_request("POST", "/public_api/v1/assets", payload)
        return data.get("reply")
Step 3: Handle HTTP Methods
The _make_request function supports GET, POST, PUT, PATCH, and DELETE. Ensure you match the method and endpoint path exactly as documented in the Cortex Cloud API reference
.

### 2. Pytest Sanity Check Module (`test_cortex_client.py`)

This test module uses `unittest.mock` to intercept the `requests` calls, allowing you to validate the client's payload generation and error-handling logic without requiring a live Cortex Cloud tenant or exposing real API keys.
