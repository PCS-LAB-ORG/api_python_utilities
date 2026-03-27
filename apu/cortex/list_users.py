import json
import pprint

import login
import requests
from requests.exceptions import HTTPError

domain, headers = login.login()
url = f"{domain}/public_api/v1/platform/iam/v1/user" # Intuitions
url = f"{domain}/platform/iam/v1/user" # Documentated 

response = requests.get(url, headers=login.headers)
try:
    response.raise_for_status()
    res_js = json.loads(response.text)
    pprint.pprint(res_js)
    # datasets = sorted(res_js['reply'], key=lambda entry: entry["Type"])
    # for data in datasets:
    #     print(f"{data['Dataset Name']}, {data['Type']}")
except HTTPError as e:
    print(e)
    if e.response.status_code == 403:
        print("Probably don't have the right permissions on these creds")
