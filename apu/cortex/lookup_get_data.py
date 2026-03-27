import json

import login
import requests
from requests.exceptions import HTTPError

domain, headers = login.login()
url = f"{domain}/public_api/v1/xql/lookups/get_data"

payload = {
    "request_data": {
        "dataset_name": "a"
    }
}

response = requests.post(url, json=payload, headers=login.headers)
try:
    response.raise_for_status()
    res_js = json.loads(response.text)
    print(res_js)
    # datasets = sorted(res_js['reply'], key=lambda entry: entry["Type"])
    # for data in datasets:
    #     print(f"{data['Dataset Name']}, {data['Type']}")
except HTTPError as e:
    print(e)
    if e.response.status_code == 403:
        js_res = json.loads(e.response.text)
        print(js_res)
        print("Probably don't have the right permissions on these creds")
