import json

import login
import requests

domain, headers = login.login()
url = f"{domain}/public_api/v1/integrations/syslog/get"

payload = {
    # "request_data": {
    #     "filters": [
    #         {"field": "name", "operator": "eq", "value": "login"}
    #     ]
    # }
}

response = requests.post(url, json=payload, headers=headers)
try:
    response.raise_for_status()
    res_js = json.loads(response.text)
    # datasets = sorted(res_js['reply'], key=lambda entry: entry["Type"])
    # for data in datasets:
    #     print(f"{data['Dataset Name']}, {data['Type']}")
except Exception as e:
    print(e)
