import json

import requests

from apu.utils import login


def get_policies(category_list, repo_id_list):
    url = f"{login.settings['url']}/bridgecrew/api/v2/errors/branch_scan/policies"
    policies = []
    has_next = True
    offset = 0
    limit = 50 # It may default to 10 when unspecified
    while has_next:
        payload = {
            "filters": {
                "repositories": repo_id_list,
                "branch": "default",
                "checkStatus": "Error",
                "codeCategories": list(category_list),
                "severities": []
            },
            "offset": offset,
            "search": {"scopes": [], "term": ""},
            "limit": limit,
            "sortBy": [
                {"key": "Severity", "direction": "DESC"},
                {"key": "Count", "direction": "DESC"},
            ],
        }
        response = requests.request("POST", url, headers=login.headers, json=payload)
        response.raise_for_status()
        js_res = json.loads(response.text)
        data = js_res['data']
        policies.extend(data)
        offset += limit
        if 'hasNext' in js_res:
            has_next = bool(js_res['hasNext'])
        else:
            has_next = False
    # print(response.text)
    return policies


def get_policies_by_resource(repository_list, resource_list):
    policy_list = []
    limit = 100
    offset = 0
    for resource in resource_list:
        has_next = True
        while has_next:
            resource_id = resource['resourceUuid']
            url = f"{login.settings['url']}/bridgecrew/api/v2/errors/branch_scan/resources/{resource_id}/policies"

            payload = json.dumps(
                {
                    "filters": {
                        "checkStatuses": [], 
                        "codeCategories": [resource['codeCategory']]
                    },
                    "codeCategory": resource['codeCategory'],
                    "limit": limit,
                    "offset": offset,
                    "sortBy": [{"key": "Severity", "direction": "DESC"}],
                }
            )

            response = requests.request("POST", url, headers=login.headers, data=payload)
            response.raise_for_status()
            policies = json.loads(response.text)
            resource_friendly_name = ""
            if "resourceName" in resource:
                resource_friendly_name = resource['resourceName']
            elif "filePath" in resource:
                resource_friendly_name = resource["filePath"]
            print(f"Found {len(policies)} more policies from {resource_friendly_name}")
            policy_list.extend(policies['data'])
            
            offset += limit
            if 'hasNext' in policies:
                has_next = bool(policies['hasNext'])
            else:
                has_next = False

    return policy_list
