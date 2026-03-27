#!/bin/bash python

# Primary API Doc link
# https://pan.dev/prisma-cloud/api/cspm/add-user-v-3/

import json
import pprint
from datetime import datetime

import requests

from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()

url = f"{login.settings["url"]}/v3/user"

payload = {}


# The API requires 13 characters in the timestamp so I add a single millisecond. The UI only shows down to the second. Rounding is assumed at this point unconfirmed.
day = datetime(2025, 6, 7, 0, 0, 0, 1)
timestamp_float = day.timestamp()
timestamp_int = int(timestamp_float)
sats = str(timestamp_float).replace(".", "")[:13]  # Get first 13 characters

service_account_role_name = "Reduced Developer Role"
service_account_role_id = ""
role_name_url = f"{login.settings["url"]}/user/role"
role_list_response = requests.request(
    "GET", role_name_url, headers=headers, data=payload
)
role_list_json = json.loads(role_list_response.text)
for role in role_list_json:
    if role["name"] == service_account_role_name:
        service_account_role_id = role["id"]

payload = json.dumps(
    {
        "accessKeyExpiration": sats,
        "accessKeyName": "miles-access-key-87",
        "defaultRoleId": service_account_role_id,  # Use a function to translate a role name here. It does not 'just work' with the role name. confirmed
        "enabled": True,
        "enableKeyExpiration": True,
        "timeZone": "America/Los_Angeles",
        "type": "SERVICE_ACCOUNT",
        "username": "miles-service-account-87",
    }
)

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(f"Request Status Code: {response.status_code}")
with open("access_key.json", "w") as access_key:
    access_key.write(response.text)
