import json

import requests
from requests.exceptions import HTTPError
from apu.cortex import login

domain, headers = login.login()
url = f"{domain}/public_api/v1/rbac/get_user_group"

payload = {
    "request_data": {
        "group_names": []
    }
}

response = requests.post(url, json=payload, headers=headers)
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
