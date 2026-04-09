#!/bin/bash python

# Primary API Doc link
# https://pan.dev/prisma-cloud/api/cspm/add-user-v-3/


import requests

from apu.utils import login

# id = "<my username>"
account_id = "miles-service-account-85"

url = f"{login.settings['url']}/user/{account_id}"

payload = {}
response = requests.request("DELETE", url, headers=login.headers, data=payload)
response.raise_for_status()
print(response)
