
import requests
from apu.cortex.login import CortexAuthManager


# ==========================================
# Request Manager & Operational Client
# ==========================================

class CortexCloudClient:
    def __init__(self, config_file="cortex.env"):
        """Initialize the client by offloading configuration to the Auth Manager."""
        self.auth = CortexAuthManager(config_file=config_file)

    def raise_on_error(self, response):
        """Evaluate HTTP status codes and Cortex-specific JSON error payloads."""
        response.raise_for_status()
        
        try:
            data = response.json()
        except ValueError:
            raise Exception(f"Failed to parse JSON response: {response.text}")

        # Extract internal application errors often wrapped in 'reply'
        error_container = data.get("reply", data)
        if isinstance(error_container, dict) and "err_code" in error_container:
            err_code = error_container["err_code"]
            if err_code not in (0, 200):
                err_msg = error_container.get("err_msg", "Unknown error")
                err_extra = error_container.get("err_extra", "No extra details provided")
                raise Exception(f"Cortex API Error [{err_code}]: {err_msg} - Details: {err_extra}")

        return data

    def _make_request(self, method, endpoint, payload=None):
        """Execute the API call using headers from the Auth Manager and run error checks."""
        url = f"{self.auth.base_url}{endpoint}"
        headers = self.auth.get_auth_headers()
        
        if method.upper() == "POST":
            response = requests.post(url, json=payload, headers=headers)
        elif method.upper() == "GET":
            response = requests.get(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return self.raise_on_error(response)



# import json

# import requests
# from requests.exceptions import HTTPError
# from apu.cortex import login

# domain, headers = login.login()

# def post(url, payload):
#     url = f"{domain}/public_api/v1/{url}"
#     response = requests.post(url, json=payload, headers=headers)
#     try:
#         response.raise_for_status()
#         res_js = json.loads(response.text)
#         return res_js
#     except HTTPError as e:
#         print(e)
#         if e.response.status_code == 403:
#             js_res = json.loads(e.response.text)
#             print(js_res)
#             print("Probably don't have the right permissions on these creds")
#         raise e

# def get(url):
#     url = f"{domain}/public_api/v1/{url}"
#     response = requests.get(url, headers=headers)
#     try:
#         response.raise_for_status()
#         res_js = json.loads(response.text)
#         return res_js
#     except HTTPError as e:
#         print(e)
#         if e.response.status_code == 403:
#             js_res = json.loads(e.response.text)
#             print(js_res)
#             print("Probably don't have the right permissions on these creds")
#         raise e
