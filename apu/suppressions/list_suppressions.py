#!python

# https://pan.dev/prisma-cloud/api/code/get-suppressions/

import os
from pathlib import Path
import pprint
import requests
import json
from prismacloud.api import pc_api


def flatten_json(nested_json):
    """
    Flattens a nested JSON object into a single-level dictionary.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

# import sys, os
# sys.path.append(os.path.abspath(f"utils"))
# import http_logging
# http_logging.http_logging()

cwd = os.path.dirname(os.path.realpath(__file__))


from prismacloud.api import pc_api
from apu.utils import login, http_logging # importing this should trigger the login procedure
# http_logging.http_logging()


headers = {
  'Accept': 'application/json; charset=UTF-8',
  'Authorization': pc_api.token
}

url = f"{settings['url']}/code/api/v1/suppressions"

response = requests.request("GET", url, headers=headers)
js_res = json.loads(response.text)
# pprint.pprint(js_res)

resources = []
tags = []
cves = []
secrets = []
policy = []
cve_accounts = []
license = []
accounts = []
for suppression in js_res:
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
