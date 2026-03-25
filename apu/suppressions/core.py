#!python

# https://pan.dev/prisma-cloud/api/code/get-suppressions/

import os
from pathlib import Path
import pprint
import requests
import json
from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

login.login(redlock=False)  # Authorization header


def get():
    url = f"{login.settings['url']}/code/api/v1/suppressions"

    response = requests.request("GET", url, headers=login.headers)
    js_res = json.loads(response.text)
    # pprint.pprint(js_res)
    return js_res


def create(category):
    if category == "Secrets":
        comment = "it's elementary"
        policy_id = "BC_GIT_9"  # "902599344975759360_SECRETS_1745427256645"
        account_id = "jumiles/webgoat"
        file_path = "/src/test/java/org/owasp/webgoat/webwolf/jwt/JWTTokenTest.java"
        commit_sha = "f4dac9065a6c93d8d93caf8a9567d9cb83688ba0"
        # expiration_time = 1756278000000

        payload = {
            "comment": comment,
            # "expirationTime":expiration_time,
            "suppressionType": "Resources",
            "resources": {
                "accountId": account_id,
                "id": f"{policy_id}::{account_id}::{file_path}:{commit_sha}",
            },
            "origin": "Platform",
        }

        url = f"{login.settings['url']}/bridgecrew/api/v1/suppressions/{policy_id}"

        response = requests.request("POST", url, headers=login.headers, data=payload)

        js_res = json.loads(response.text)
        pprint.pprint(js_res)
    return js_res

    # curl 'https://api2.prismacloud.io/bridgecrew/api/v1/suppressions/$policyId' \
    #   -H 'Authorization: ...' \
    #   -H 'Accept: application/json, text/plain, */*' \
    #   -H 'Content-Type: application/json' \
    #   --data-raw $'{"comment":$comment,"expirationTime":1756278000000,"suppressionType":"Resources","resources":{"accountId":"jumiles-pa/test-cas-app","id":"$policyId::jumiles-pa/test-cas-app::/README.md:3ac743df70f6d3b34bceee4753eeeedaa4650911"},"origin":"Platform"}'


#   create_suppression(comment, policy_id, account_id, derived_file_path_with_commit, code_lines, expiration)
def create_suppression(comment, policyId, account_id, file_path, code_lines, expiration=-1, uuid="", category=""):
    # https://pan.dev/prisma-cloud/api/code/create-suppression/

    '''
    Suppression Types:
    SecretsPolicy
    PackageLicense
    LicenseType
    CvesAccounts
    OrganizationAndPolicy
    Tags
    Accounts
    Policy
    Cves
    '''

    # resource uuid and policy uuid are matching and represent the finding id needed for weaknesses
    if category == "Weaknesses":
        
        url = f"{login.settings['url']}/bridgecrew/api/v1/suppressions"
        payload_js = {
            "policyIds": [policyId],
            "justificationComment": comment,
            "ruleType": "finding",
            "type": "PERIODIC",
            "findingIds": [uuid]
        }
        # I need to check how it does this...
        if not expiration == -1:
            # Valentines Day 2026 at 12:00am PST
            # {"comment":"asdf","expirationTime":1771056000000,"suppressionType":"Resources","resources":{"accountId":"jumiles/webgoat","id":"BC_GIT_6::jumiles/webgoat::/src/test/java/org/owasp/webgoat/lessons/missingac/MissingFunctionACUsersTest.java:91a33f0e448feb0845cba10cb0d9ac38cf19294d"},"origin":"Platform"}
            payload_js["expiration"] = expiration
        
    if category == "Secrets":
        url = f"{login.settings['url']}/bridgecrew/api/v1/suppressions/{policyId}"
        payload_js = {
            "comment": f"{today} {policyId}::{account_id}::{file_path} {code_lines}\nComment: {comment}",
            "suppressionType": "Resources",
            "resources": {
                "accountId": account_id,
                "id": f"{policyId}::{account_id}::{file_path}"
            },
            "origin": "Platform"
        }
        if not expiration == -1:
            # Valentines Day 2026 at 12:00am PST
            # {"comment":"asdf","expirationTime":1771056000000,"suppressionType":"Resources","resources":{"accountId":"jumiles/webgoat","id":"BC_GIT_6::jumiles/webgoat::/src/test/java/org/owasp/webgoat/lessons/missingac/MissingFunctionACUsersTest.java:91a33f0e448feb0845cba10cb0d9ac38cf19294d"},"origin":"Platform"}
            payload_js["expiration"] = expiration
    payload = json.dumps(payload_js)

    response = requests.request("POST", url, headers=login.headers, data=payload)
    response.raise_for_status()
    print(f"Suppressed: {response.text} {account_id} {policyId}::{account_id}::{file_path} {comment}")

def delete(policy, suppression):
    suppression_id = suppression['id']  # UUID Format
    policy_id = policy['policyId']  # like BC_GIT_2

    url = f"{login.settings['url']}/api/v1/suppressions/{policy_id}/justifications/{suppression_id}"
    response = requests.request("DELETE", url, headers=login.headers)
    js_res = json.loads(response.text)
    return js_res


def output_by_category(suppression_list):
    resources = []
    tags = []
    cves = []
    secrets = []
    policy = []
    cve_accounts = []
    license = []
    accounts = []
    for suppression in suppression_list:
        match suppression["suppressionType"]:
            case "Resources":
                resources.append(suppression)
            case "Tags":
                tags.append(suppression)
            case "Cves":
                cves.append(suppression)
            case "SecretsPolicy":
                secrets.append(suppression)
            case "Policy":
                policy.append(suppression)
            case "CvesAccounts":
                cve_accounts.append(suppression)
            case "LicenseType":
                license.append(suppression)
            case "Accounts":
                accounts.append(suppression)
            case _:
                print(suppression)

    cwd = os.path.dirname(os.path.realpath(__file__))
    folder_path = f"{cwd}/output"
    # Create the directory and all parent directories if they don't exist
    os.makedirs(folder_path, exist_ok=True)
    with open(f"{cwd}/output/resources.json", "w") as resources_file:
        json.dump(resources, resources_file, indent=4)
    with open(f"{cwd}/output/tags.json", "w") as tags_file:
        json.dump(tags, tags_file, indent=4)
    with open(f"{cwd}/output/cve.json", "w") as cve_file:
        json.dump(cves, cve_file, indent=4)
    with open(f"{cwd}/output/secrets.json", "w") as secrets_file:
        json.dump(secrets, secrets_file, indent=4)
    with open(f"{cwd}/output/policy.json", "w") as policy_file:
        json.dump(policy, policy_file, indent=4)
    with open(f"{cwd}/output/cve_accounts.json", "w") as cve_accounts_file:
        json.dump(cve_accounts, cve_accounts_file, indent=4)
    with open(f"{cwd}/output/license.json", "w") as license_file:
        json.dump(license, license_file, indent=4)
    with open(f"{cwd}/output/accounts.json", "w") as accounts_file:
        json.dump(accounts, accounts_file, indent=4)


suppression_list = get()
output_by_category(suppression_list=suppression_list)
