from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional

from apu.cortex.jrequest import CortexCloudClient

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
    timeframe: Dict[str, Any] = field(
        default_factory=lambda: {"relativeTime": 86400000}
    )


@dataclass
class XqlQueryResultsRequestData:
    query_id: str
    pending_flag: bool = False
    limit: int = 1000
    format: str = "json"


# ==========================================
# Cortex Cloud Client
# ==========================================


class CortexCloud:

    def __init__(self, config_file="cortex.env"):
        self.client = CortexCloudClient(config_file)

    # ==========================================
    # Operational Logic Methods
    # ==========================================

    def get_all_assets(self):
        """
        Retrieve detailed information about all assets in the environment.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Asset-inventory
        """
        payload = {"request_data": {}}
        data = self.client.make_request("POST", "/public_api/v1/assets", payload)
        return data.get("reply")

    def get_all_endpoints(self):
        """
        Retrieve a list of all endpoints managed by Cortex.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-all-Endpoints
        """
        payload = {"request_data": {}}
        data = self.client.make_request(
            "POST", "/public_api/v1/endpoints/get_endpoints", payload
        )
        return data.get("reply")

    def start_xql_query(self, query_data: XqlQueryRequestData):
        """
        Start an XQL query using a type-safe dataclass object.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Start-an-XQL-query/
        """
        payload = {
            "request_data": {
                k: v for k, v in asdict(query_data).items() if v is not None
            }
        }
        data = self.client.make_request(
            "POST", "/public_api/v1/xql/start_xql_query", payload
        )
        return data.get("reply")

    def get_xql_query_results(self, results_data: XqlQueryResultsRequestData):
        """
        Retrieve the results of an executed XQL query.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-XQL-query-results/
        """
        payload = {
            "request_data": {
                k: v for k, v in asdict(results_data).items() if v is not None
            }
        }
        data = self.client.make_request(
            "POST", "/public_api/v1/xql/get_query_results", payload
        )
        return data.get("reply")

    def get_cases(self):
        """Retrieve a list of cases (incidents)."""
        payload = {
            "request_data": {
                "search_from": 0,
                "search_to": 100,
                "sort": {"field": "creation_time", "keyword": "desc"},
            }
        }
        data = self.client.make_request("POST", "/public_api/v1/case/search", payload)
        return data.get("reply")

    def search_cases(self, search_data: SearchRequestData):
        """
        Search cases using a type-safe dataclass object.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Retrieve-cases-based-on-filters/
        """
        payload = {
            "request_data": {
                k: v for k, v in asdict(search_data).items() if v is not None
            }
        }
        data = self.client.make_request("POST", "/public_api/v1/case/search", payload)
        return data.get("reply")

    # ==========================================
    # Platform & System APIs
    # ==========================================

    def get_healthcheck(self):
        """
        Perform a health check of your Cortex Cloud environment.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/System-Health-Check/
        """
        data = self.client.make_request("GET", "/public_api/v1/healthcheck")
        return data

    def get_api_keys(self, payload: dict):
        """
        Get a list of API keys filtered by expiration date, role, or ID.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-existing-API-keys/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/api_keys/get_api_keys", payload
        )
        return data.get("reply")

    def get_tenant_info(self, payload: dict):
        """
        Get information about the Cortex Cloud tenant.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-Tenant-Info/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/system/get_tenant_info", payload
        )
        return data.get("reply")

    # ==========================================
    # Asset & Inventory APIs
    # ==========================================

    def get_assets(self, payload: dict):
        """
        Retrieve detailed information about all assets within your environment.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-all-or-filtered-assets/
        """
        data = self.client.make_request("POST", "/public_api/v1/assets", payload)
        return data.get("reply")

    def get_asset_by_id(self, asset_id: str):
        """
        Get the details of the asset specified by asset ID.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-asset-by-ID/
        """
        data = self.client.make_request("GET", f"/public_api/v1/assets/{asset_id}")
        return data.get("reply")

    def get_asset_groups(self, payload: dict):
        """
        Get a list of asset groups based on applied filters.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-all-or-filtered-asset-groups/
        """
        data = self.client.make_request("POST", "/public_api/v1/asset-groups", payload)
        return data.get("reply")

    # ==========================================
    # Endpoint Management APIs
    # ==========================================

    def get_endpoints(self, payload: dict):
        """
        Gets a list of all of your endpoints.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-all-Endpoints/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/endpoints/get_endpoints", payload
        )
        return data.get("reply")

    def isolate_endpoints(self, payload: dict):
        """
        Isolate one or more endpoints in a single request.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Isolate-Endpoints/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/endpoints/isolate", payload
        )
        return data.get("reply")

    def run_script(self, payload: dict):
        """
        Execute a Python script on selected endpoints.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Run-Script/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/scripts/run_script", payload
        )
        return data.get("reply")

    # ==========================================
    # Cloud Onboarding APIs (CSPM)
    # ==========================================

    def create_cloud_instance_template(self, payload: dict):
        """
        Create a template to facilitate the seamless setup of CSP data in Cortex.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Create-a-cloud-onboarding-integration-template/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/cloud_onboarding/create_instance_template", payload
        )
        return data.get("reply")

    def get_cloud_instances(self, payload: dict):
        """
        Get the configuration details of all or filtered integration instances.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-all-or-filtered-integration-instances/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/cloud_onboarding/get_instances", payload
        )
        return data.get("reply")

    def create_outpost_template(self, payload: dict):
        """
        Create a template to onboard a custom scanning outpost.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Create-an-outpost-template/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/cloud_onboarding/create_outpost_template", payload
        )
        return data.get("reply")

    # ==========================================
    # Application Security (AppSec) APIs
    # ==========================================

    def get_appsec_repositories(self, payload: dict = None):
        """
        Get details on all repositories integrated with Cortex Cloud Application Security.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-repositories/
        """
        data = self.client.make_request(
            "GET", "/public_api/appsec/v1/repositories", payload
        )
        return data

    def get_appsec_policies(self, payload: dict = None):
        """
        List all or filtered Application Security policies.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/List-AppSec-policies/
        """
        data = self.client.make_request(
            "GET", "/public_api/appsec/v1/policies", payload
        )
        return data

    def get_appsec_scan_issues(self, scan_id: str):
        """
        Get a list of the issues discovered in the specific AppSec scan.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/List-AppSec-scan-issues/
        """
        data = self.client.make_request(
            "GET", f"/public_api/appsec/v1/scans/{scan_id}/issues"
        )
        return data

    # ==========================================
    # Cloud Workload Protection (CWP) APIs
    # ==========================================
    def get_cwp_policies(self, payload: dict = None):
        """
        Get all CWP policies.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-CWP-policies/
        """
        data = self.client.make_request("GET", "/public_api/v2/cwp/policies", payload)
        return data

    def get_asset_sbom(
        self, asset_id: str, format_type: str = "json", output_format: str = "CycloneDX"
    ):
        """
        Get the Software Bill of Materials (SBOM) of the specified asset.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-the-SBOM-of-the-specified-asset/
        """
        endpoint = f"/public_api/v1/assets/{asset_id}/sbom?format={format_type}&output_format={output_format}"
        data = self.client.make_request("GET", endpoint)
        return data

    # ==========================================
    # Vulnerability Management APIs
    # ==========================================

    def get_vulnerabilities(self, payload: dict):
        """
        Get a list of vulnerabilities that match the filter fields.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/Get-list-of-vulnerabilities/
        """
        data = self.client.make_request(
            "POST", "/public_api/uvem/v1/get_vulnerabilities", payload
        )
        return data.get("reply")

    def trigger_vulnerability_scan(self, payload: dict):
        """
        Trigger an On-demand Scan based on AssetId.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/
        """
        data = self.client.make_request(
            "POST", "/public_api/vulnerability-management/v1/scan", payload
        )
        return data

    # ==========================================
    # Compliance APIs
    # ==========================================

    def get_compliance_reports(self, payload: dict):
        """
        Retrieve compliance reports/assessment profile results.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/compliance/get_reports", payload
        )
        return data.get("reply")

    def get_compliance_controls(self, payload: dict):
        """
        Retrieve compliance control details with optional filtering.
        Docs: https://docs-cortex.paloaltonetworks.com/r/Cortex-Cloud-Platform-APIs/
        """
        data = self.client.make_request(
            "POST", "/public_api/v1/compliance/get_controls", payload
        )
        return data.get("reply")
