#!/bin/bash python

import json
import pprint

import requests

from apu.utils import (
    login,
    # http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()


payload = {}

url = f"{login.settings["url"]}/user/role"

response = requests.request("GET", url, headers=login.headers, data=payload)

json_role = json.loads(response.text)
for role in json_role:
    if role["name"] == "Reduced Developer Role":
        pprint.pprint(role)
