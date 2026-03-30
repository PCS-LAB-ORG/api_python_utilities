import os
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional
import requests
import yaml
from dotenv import load_dotenv

# ==========================================
# Type-Safe Payload Objects
# ==========================================

@dataclass
class Filter:
    field: str
    operator: str
    value: Any

@dataclass
class Sort:
    field: str
    keyword: str  # 'asc' or 'desc'

@dataclass
class SearchRequestData:
    search_from: int = 0
    search_to: int = 100
    sort: Optional[Sort] = None
    filters: Optional[List[Filter]] = None

@dataclass
class XqlQueryRequestData:
    query: str
    tenants: List[str] = field(default_factory=list)
    timeframe: Dict[str, Any] = field(default_factory=lambda: {"relativeTime": 86400000})

@dataclass
class XqlQueryResultsRequestData:
    query_id: str
    pending_flag: bool = False
    limit: int = 1000
    format: str = "json"

# ==========================================
# Cortex Cloud Client
# ==========================================

class CortexCloudClient:
    def __init__(self, config_file="cortex.env"):
        """
        Initialize the client. It uses python-dotenv to load a .env file,
        then falls back to a .yaml configuration if required.
        """
        # 1. If it's an environment file, use dotenv to inject it directly into os.environ
        if config_file.endswith('.env') or "env" in config_file:
            if os.path.exists(config_file):
                load_dotenv(dotenv_path=config_file)

        # 2. Extract credentials from environment variables 
        # (which now includes anything loaded by dotenv)
        self.base_url = os.environ.get("CORTEX_API_BASE_URL")
        self.api_key_id = os.environ.get("CORTEX_API_KEY_ID")
        self.api_key = os.environ.get("CORTEX_API_KEY")

        # 3. Fallback to YAML configuration if vars are still missing and a .yaml was provided
        if not all([self.base_url, self.api_key_id, self.api_key]) and config_file.endswith(('.yaml', '.yml')):
            self._load_credentials_from_yaml(config_file)

        # Final Validation
        if not all([self.base_url, self.api_key_id, self.api_key]):
            raise ValueError("Credentials missing. Ensure CORTEX_API_BASE_URL, CORTEX_API_KEY_ID, and CORTEX_API_KEY are set in your environment or config file.")

        # Ensure proper URL formatting
        if not self.base_url.startswith("http"):
            self.base_url = f"https://{self.base_url}"

    def _load_credentials_from_yaml(self, config_file: str):
        """Extract credentials from a .cortex.yaml file."""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f) or {}
                self.base_url = self.base_url or config.get("CORTEX_API_BASE_URL")
                self.api_key_id = self.api_key_id or str(config.get("CORTEX_API_KEY_ID", ""))
                self.api_key = self.api_key or config.get("CORTEX_API_KEY")

    def _get_auth_headers(self):
        """Construct the required authentication headers."""
        return {
            "x-xdr-auth-id": self.api_key_id,
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def raise_on_error(self, response):
        """Evaluate HTTP status codes and Cortex-specific JSON error payloads."""
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            raise Exception(f"Failed to parse JSON response: {response.text}")

        error_container = data.get("reply", data)
        if isinstance(error_container, dict) and "err_code" in error_container:
            err_code = error_container["err_code"]
            if err_code not in (0, 200):
                err_msg = error_container.get("err_msg", "Unknown error")
                err_extra = error_container.get("err_extra", "No extra details provided")
                raise Exception(f"Cortex API Error [{err_code}]: {err_msg} - Details: {err_extra}")

        return data

    def _make_request(self, method, endpoint, payload=None):
        """Execute the API call and run the error check."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_auth_headers()

        if method.upper() == "POST":
            response = requests.post(url, json=payload, headers=headers)
        elif method.upper() == "GET":
            response = requests.get(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        return self.raise_on_error(response)

    # ==========================================
    # Operational Logic Methods
    # ==========================================

    def search_cases(self, search_data: SearchRequestData):
        """Search cases using a type-safe dataclass object."""
        payload = {"request_data": {k: v for k, v in asdict(search_data).items() if v is not None}}
        data = self._make_request("POST", "/public_api/v1/case/search", payload)
        return data.get("reply")


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

    # ==========================================
    # Platform & System APIs
    # ==========================================

    def get_healthcheck(self):
        """Perform a health check of your Cortex Cloud environment."""
        data = self._make_request("GET", "/public_api/v1/healthcheck")
        return data

    def get_api_keys(self, payload: dict):
        """Get a list of API keys filtered by expiration date, role, or ID."""
        data = self._make_request("POST", "/public_api/v1/api_keys/get_api_keys", payload)
        return data.get("reply")

    def get_tenant_info(self, payload: dict):
        """Get information about the Cortex Cloud tenant."""
        data = self._make_request("POST", "/public_api/v1/system/get_tenant_info", payload)
        return data.get("reply")

    # ==========================================
    # Asset & Inventory APIs
    # ==========================================

    def get_assets(self, payload: dict):
        """Retrieve detailed information about all assets within your environment."""
        data = self._make_request("POST", "/public_api/v1/assets", payload)
        return data.get("reply")

    def get_asset_by_id(self, asset_id: str):
        """Get the details of the asset specified by asset ID."""
        data = self._make_request("GET", f"/public_api/v1/assets/{asset_id}")
        return data.get("reply")

    def get_asset_groups(self, payload: dict):
        """Get a list of asset groups based on applied filters."""
        data = self._make_request("POST", "/public_api/v1/asset-groups", payload)
        return data.get("reply")

    # ==========================================
    # Endpoint Management APIs
    # ==========================================

    def get_endpoints(self, payload: dict):
        """Gets a list of all of your endpoints."""
        data = self._make_request("POST", "/public_api/v1/endpoints/get_endpoints", payload)
        return data.get("reply")

    def isolate_endpoints(self, payload: dict):
        """Isolate one or more endpoints in a single request."""
        data = self._make_request("POST", "/public_api/v1/endpoints/isolate", payload)
        return data.get("reply")

    def run_script(self, payload: dict):
        """Execute a Python script on selected endpoints."""
        data = self._make_request("POST", "/public_api/v1/scripts/run_script", payload)
        return data.get("reply")

    # ==========================================
    # Cloud Onboarding APIs (CSPM)
    # ==========================================

    def create_cloud_instance_template(self, payload: dict):
        """Create a template to facilitate the seamless setup of CSP data in Cortex."""
        data = self._make_request("POST", "/public_api/v1/cloud_onboarding/create_instance_template", payload)
        return data.get("reply")

    def get_cloud_instances(self, payload: dict):
        """Get the configuration details of all or filtered integration instances."""
        data = self._make_request("POST", "/public_api/v1/cloud_onboarding/get_instances", payload)
        return data.get("reply")

    def create_outpost_template(self, payload: dict):
        """Create a template to onboard a custom scanning outpost."""
        data = self._make_request("POST", "/public_api/v1/cloud_onboarding/create_outpost_template", payload)
        return data.get("reply")

    # ==========================================
    # Application Security (AppSec) APIs
    # ==========================================

    def get_appsec_repositories(self, payload: dict = None):
        """Get details on all repositories integrated with Cortex Cloud Application Security."""
        # AppSec APIs often use GET with query parameters instead of POST with a body
        data = self._make_request("GET", "/public_api/appsec/v1/repositories", payload)
        return data

    def get_appsec_policies(self, payload: dict = None):
        """List all or filtered Application Security policies."""
        data = self._make_request("GET", "/public_api/appsec/v1/policies", payload)
        return data

    def get_appsec_scan_issues(self, scan_id: str):
        """Get a list of the issues discovered in the specific AppSec scan."""
        data = self._make_request("GET", f"/public_api/appsec/v1/scans/{scan_id}/issues")
        return data

    # ==========================================
    # Cloud Workload Protection (CWP) APIs
    # ==========================================

    def get_cwp_policies(self, payload: dict = None):
        """Get all CWP policies."""
        data = self._make_request("GET", "/public_api/v2/cwp/policies", payload)
        return data

    def get_asset_sbom(self, asset_id: str, format_type: str = "json", output_format: str = "CycloneDX"):
        """Get the Software Bill of Materials (SBOM) of the specified asset."""
        # Requires query parameters: format, output_format, attributes
        endpoint = f"/public_api/v1/assets/{asset_id}/sbom?format={format_type}&output_format={output_format}"
        data = self._make_request("GET", endpoint)
        return data

    # ==========================================
    # Vulnerability Management APIs
    # ==========================================

    def get_vulnerabilities(self, payload: dict):
        """Get a list of vulnerabilities that match the filter fields."""
        data = self._make_request("POST", "/public_api/uvem/v1/get_vulnerabilities", payload)
        return data.get("reply")

    def trigger_vulnerability_scan(self, payload: dict):
        """Trigger an On-demand Scan based on AssetId."""
        data = self._make_request("POST", "/public_api/vulnerability-management/v1/scan", payload)
        return data

    # ==========================================
    # Compliance APIs
    # ==========================================

    def get_compliance_reports(self, payload: dict):
        """Retrieve compliance reports."""
        data = self._make_request("POST", "/public_api/v1/compliance/get_reports", payload)
        return data.get("reply")

    def get_compliance_controls(self, payload: dict):
        """Retrieve compliance control details with optional filtering."""
        data = self._make_request("POST", "/public_api/v1/compliance/get_controls", payload)
        return data.get("reply")

# Example Usage:
# client = CortexCloudClient(fqdn="api-tenant.xdr.us.paloaltonetworks.com", api_key_id="123", api_key="your_secret_key")
# try:
#     endpoints = client.get_all_endpoints()
#     print(endpoints)
# except Exception as e:
#     print(f"Operational task failed: {e}")