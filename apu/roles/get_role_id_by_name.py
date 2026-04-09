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

response = requests.request(
    "GET", f"{login.settings['url']}/role", headers=login.headers, data=payload
)

json_role = json.loads(response.text)
for role in json_role:
    if role["name"] == "Test role":
        pprint.pprint(role)
