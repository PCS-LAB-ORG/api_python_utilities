# give me a python module to call each cortex API and raise_on_error() check results so I can use this as a library for operational logic


import requests
import json

class CortexCloudClient:
    def __init__(self, fqdn, api_key_id, api_key):
        """
        Initialize the Cortex Cloud API Client.
        fqdn: Your tenant's Fully Qualified Domain Name (e.g., api-mycompany.xdr.us.paloaltonetworks.com)
        """
        self.base_url = f"https://{fqdn}"
        self.api_key_id = str(api_key_id)
        self.api_key = api_key

    def _get_auth_headers(self):
        """Construct the required authentication headers."""
        return {
            "x-xdr-auth-id": self.api_key_id,
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def raise_on_error(self, response):
        """
        Check for HTTP errors and Cortex-specific JSON error structures.
        Raises an exception if the API request failed.
        """
        # 1. Check for standard HTTP errors (e.g., 401 Unauthorized, 403 Forbidden, 500 Internal Error)
        response.raise_for_status()
        
        # 2. Parse the JSON response
        try:
            data = response.json()
        except ValueError:
            raise Exception(f"Failed to parse JSON response: {response.text}")

        # 3. Check for Cortex-specific application errors embedded in the payload
        # Cortex APIs often return errors inside a 'reply' or at the root level with 'err_code'
        error_container = data.get("reply", data)
        
        if isinstance(error_container, dict) and "err_code" in error_container:
            err_code = error_container["err_code"]
            # Cortex considers 200 and 0 as successful status codes internally in many endpoints
            if err_code not in (0, 200):
                err_msg = error_container.get("err_msg", "Unknown error")
                err_extra = error_container.get("err_extra", "No extra details provided")
                raise Exception(f"Cortex API Error [{err_code}]: {err_msg} - Details: {err_extra}")

        return data

    def _make_request(self, method, endpoint, payload=None):
        """Generic method to make API calls and validate results."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_auth_headers()
        
        if method.upper() == "POST":
            response = requests.post(url, json=payload, headers=headers)
        elif method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=payload, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return self.raise_on_error(response)

    # ==========================================
    # Operational Logic Methods
    # ==========================================

    def start_xql_query(self, query):
        """
        Start an XQL query. 
        Returns the execution ID which can be used to retrieve results.
        """
        payload = {
            "request_data": {
                "query": query,
                "timeframe": {"relativeTime": 86400000} # Last 24 hours
            }
        }
        data = self._make_request("POST", "/public_api/v1/xql/start_xql_query", payload)
        return data.get("reply")

    def get_xql_query_results(self, query_id):
        """Retrieve the results of an executed XQL query."""
        payload = {
            "request_data": {
                "query_id": query_id,
                "pending_flag": False,
                "limit": 1000,
                "format": "json"
            }
        }
        data = self._make_request("POST", "/public_api/v1/xql/get_query_results", payload)
        return data.get("reply")

    def get_all_assets(self):
        """Retrieve detailed information about all assets in the environment."""
        payload = {"request_data": {}}
        data = self._make_request("POST", "/public_api/v1/assets", payload)
        return data.get("reply")

    def get_all_endpoints(self):
        """Retrieve a list of all endpoints managed by Cortex."""
        payload = {"request_data": {}}
        data = self._make_request("POST", "/public_api/v1/endpoints/get_endpoints", payload)
        return data.get("reply")

    def get_cases(self):
        """Retrieve a list of cases (incidents)."""
        payload = {
            "request_data": {
                "search_from": 0,
                "search_to": 100,
                "sort": {
                    "field": "creation_time",
                    "keyword": "desc"
                }
            }
        }
        data = self._make_request("POST", "/public_api/v1/case/search", payload)
        return data.get("reply")

# Example Usage:
# client = CortexCloudClient(fqdn="api-tenant.xdr.us.paloaltonetworks.com", api_key_id="123", api_key="your_secret_key")
# try:
#     endpoints = client.get_all_endpoints()
#     print(endpoints)
# except Exception as e:
#     print(f"Operational task failed: {e}")