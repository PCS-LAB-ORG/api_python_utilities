import os
import requests
import json
import pprint
from pathlib import Path
from dotenv import dotenv_values
from requests.exceptions import HTTPError

import login

domain, headers = login.login()
url = f"{domain}/public_api/v1/platform/iam/v1/user" # Intuitions
url = f"{domain}/platform/iam/v1/user" # Documentated 

response = requests.get(url, headers=headers)
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
