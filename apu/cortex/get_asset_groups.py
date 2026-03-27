import json
import pprint

import requests
from requests.exceptions import HTTPError
from apu.cortex import login

domain, headers = login.login()
url = f"{domain}/public_api/v1/asset-groups"

payload = {
    "request_data": {
        #     "AND": [
        #         {
        #             "SEARCH_FIELD": "XDM.ASSET_GROUP.TYPE",
        #             "SEARCH_TYPE": "EQ",
        #             "SEARCH_VALUE": "Dynamic",
        #         }
        #     ]
        # },
        # "sort": [{"FIELD": "XDM.ASSET_GROUP.LAST_UPDATE_TIME", "ORDER": "DESC"}],
        # "search_from": 0,
        # "search_to": 1000,
    }
}

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
        js_res = json.loads(e.response.text)
        print(js_res)
        print("Probably don't have the right permissions on these creds")
