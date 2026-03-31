import json

import requests

from apu.utils import login


# This is only for branch scans not for pull request and CICD scans (checkov)
# def get_resources_by_policies(policy_list, category_list, repo_id_list):
def get_resources_by_policies(policy_entries):

    resource_list = []
    policy_id_list = set()
    offset = 0
    limit = 100
    # for category in list(category_list):
    for entry in policy_entries:

        has_next = True
        # https://api2.prismacloud.io/bridgecrew/api/v2/errors/branch_scan/policies/BC_GIT_9/resources
        while has_next:
            url = f"{login.settings['url']}/bridgecrew/api/v2/errors/branch_scan/policies/{entry['policy_id']}/resources"

            # Confirm that checkStatuses Errors works
            payload = json.dumps(
                {
                    "filters": {
                        # "checkStatuses": ['Errors'],
                        # "codeCategories": list(category_list),
                        "repositories": entry["repo_id_list"]
                    },
                    "codeCategory": entry["category"],
                    "limit": limit,
                    "offset": offset,
                    "sortBy": [{"key": "Severity", "direction": "DESC"}],
                }
            )

            response = requests.request(
                "POST", url, headers=login.headers, data=payload
            )
            try:
                response.raise_for_status()
                js_res = json.loads(response.text)
                resource_list.extend(js_res["data"])
                resounce_length = len(js_res["data"])
                print(
                    f"Found {resounce_length} more resources from {entry['policy_id']} {entry['repo_id_list'][:10]}..."
                )
                if 0 == resounce_length:
                    has_next = False

                offset += limit
                if "hasNext" in js_res:
                    has_next = bool(js_res["hasNext"])
                else:
                    has_next = False
            except Exception as e:
                print(e)
        if 0 == resounce_length:
            break
            # continue
    return resource_list


# This is only for pull request and CICD scans (checkov) not for branch scans
def get_resources_by_policies_checkov(policy_list, category_repo_list_map):

    resource_list = []
    policy_id_list = set()
    offset = 0
    limit = 100
    for policy in policy_list:
        has_next = True
        # https://api2.prismacloud.io/bridgecrew/api/v2/errors/code-issues/code_review_scan/policies/BC_GIT_9/resources
        while has_next:
            url = f"{login.settings['url']}/bridgecrew/api/v2/errors/branch_scan/policies/{policy['policyId']}/resources"

            # Confirm that checkStatuses Errors works
            payload = json.dumps(
                {
                    "filters": {
                        # "checkStatuses": ['Errors'],
                        #     "codeCategories": ["ThirdPartyWeaknesses"],
                        "repositories": repository_list
                    },
                    "codeCategory": "Secrets",
                    "limit": limit,
                    "offset": offset,
                    "sortBy": [{"key": "Severity", "direction": "DESC"}],
                }
            )

            response = requests.request(
                "POST", url, headers=login.headers, data=payload
            )
            try:
                response.raise_for_status()
                js_res = json.loads(response.text)
                resource_list.extend(js_res["data"])

                offset += limit
                if "hasNext" in js_res:
                    has_next = bool(js_res["hasNext"])
                else:
                    has_next = False
            except Exception as e:
                print(e)
    return resource_list
