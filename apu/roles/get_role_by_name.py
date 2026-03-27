#!/bin/bash python

import requests
import json
import pprint



from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()


payload = {}

response = requests.request("GET", url, headers=login.headers, data=payload)

json_role = json.loads(response.text)
for role in json_role:
    if role["name"] == "Reduced Developer Role":
        pprint.pprint(role)
