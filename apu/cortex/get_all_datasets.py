import os
import requests
import json
import pprint
from pathlib import Path
from dotenv import dotenv_values

config = dotenv_values(f"{Path.home()}/.cortexcloud/lab.py")

# CORTEX_API_KEY_ID=config["CORTEX_API_KEY_ID"]
# CORTEX_API_KEY=config["CORTEX_API_KEY"]
# DOMAIN = config["CORTEX_DOMAIN"]

url = f"{config.get('CORTEX_DOMAIN')}/public_api/v1/xql/get_datasets"

payload = { "request_data": {} }
headers = {
    "Authorization": config.get('CORTEX_API_KEY'),
    "x-xdr-auth-id": config.get('CORTEX_API_KEY_ID'),
    "Content-Type": "application/json",
    "Accept": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()
res_js = json.loads(response.text)
datasets = sorted(res_js['reply'], key=lambda entry: entry["Type"])
for data in datasets:
    print(f"{data['Dataset Name']}, {data['Type']}")
