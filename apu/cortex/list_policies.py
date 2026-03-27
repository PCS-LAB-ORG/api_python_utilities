import os
import requests
import json
import pprint
from pathlib import Path
from dotenv import dotenv_values
from requests.exceptions import HTTPError

import login

domain, headers = login.login()
url = f"{domain}/public_api/v1/policy/search"

payload = {
    "filter": {
        "AND": [
            # {
            #     "SEARCH_FIELD": "id",
            #     "SEARCH_TYPE": "CONTAINS",
            #     "SEARCH_VALUE": "b2b1279e-8760-44a8-8dca-bcc4508f8ce7",
            # },
            # {
            #     "SEARCH_FIELD": "name",
            #     "SEARCH_TYPE": "CONTAINS",
            #     "SEARCH_VALUE": "Cloud Posture Security",
            # },
        ]
    },
    "search_from": 0,
    "search_to": 500,
    "sort": [{"FIELD": "name", "ORDER": "ASC"}],
} # This works as-is 3/26/2026

response = requests.post(url, json=payload, headers=headers)
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
