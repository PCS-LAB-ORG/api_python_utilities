import sys
import os
import requests
import json
import pprint
from dotenv import dotenv_values
from pathlib import Path


config = dotenv_values(f"{Path.home()}/.cortexcloud/lab.py")
url = f"{config.get('CORTEX_DOMAIN')}/public_api/v1/xql/lookups/get_data"

if not len(sys.argv) > 1:
    raise("Table name is required")
dataset_name = sys.argv[1]

limit = 20
if len(sys.argv) > 2:
    limit = int(sys.argv[2])

filters = []
if len(sys.argv) > 3:
    filters = json.loads(sys.argv[3])
# [
    # {
    #     # "uid": "123",
    #     "user_email": "hiep@abc.com"
    # },
    # {
    #     "department": "dev",
    #     "zipcode": "58674"
    # }
# ],

payload = { 
    "request": {
        "dataset_name": dataset_name,
        "filters": filters,
        "limit": limit
    }
}
headers = {
    "Authorization": config.get("CORTEX_API_KEY"),
    "x-xdr-auth-id": config.get("CORTEX_API_KEY_ID"),
    "Accept-Encoding": "",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
try:
    response.raise_for_status()
    js_res = json.loads(response.text)
    pprint.pprint(js_res)
except Exception as e:
    print(e)
    # print(response.request.url)
    # print(response.request.headers)
    # print(response.request.body)
