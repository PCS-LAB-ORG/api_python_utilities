#!/bin/bash python

import json
import os
import pprint
import sys

import requests
from prismacloud.api import pc_api

from apu.utils import login

url = f"{login.settings['url']}/v3/user"


payload = {}

response = requests.request("GET", url, headers=login.headers, data=payload)

service_accounts = []
user_list = json.loads(response.text)
for user in user_list:
    if user["type"] == "SERVICE_ACCOUNT":
        pprint.pprint(user)
        service_accounts.append(user)
