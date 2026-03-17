#!/bin/bash python

# Primary API Doc link
# https://pan.dev/prisma-cloud/api/cspm/add-user-v-3/

import requests
import json
import pprint, sys, os
from pathlib import Path
from datetime import datetime

from prismacloud.api import pc_api

from pathlib import Path
sys.path.append(os.path.abspath(f".."))
from creds_lab import PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY

#############################################################################################
# This section would turn on extra logging for http requests
#############################################################################################
def http_logging():
  import logging

  # These two lines enable debugging at httplib level (requests->urllib3->http.client)
  # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
  # The only thing missing will be the response.body which is not logged.
  try:
      import http.client as http_client
  except ImportError:
      # Python 2
      import httplib as http_client
  http_client.HTTPConnection.debuglevel = 1

  # You must initialize logging, otherwise you'll not see debug output.
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  requests_log = logging.getLogger("requests.packages.urllib3")
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True
# http_logging() # Uncomment for extra logging (curl -v)

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": "https://api2.prismacloud.io",
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}
# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

url = f"{settings["url"]}/v3/user"

pc_api.configure(settings=settings)

payload = {}
headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': '*/*',
  'x-redlock-auth': pc_api.token,
}

from datetime import date
# The API requires 13 characters in the timestamp so I add a single millisecond. The UI only shows down to the second. Rounding is assumed at this point unconfirmed.
day = datetime(2025, 6, 7, 0, 0, 0, 1)
timestamp_float = day.timestamp()
timestamp_int = int(timestamp_float)
sats = str(timestamp_float).replace(".", "")[:13] # Get first 13 characters

service_account_role_name = "Reduced Developer Role"
service_account_role_id = ""
role_name_url = f"{settings["url"]}/user/role"
role_list_response = requests.request("GET", role_name_url, headers=headers, data=payload)
role_list_json = json.loads(role_list_response.text)
for role in role_list_json:
    if role["name"] == service_account_role_name:
        service_account_role_id = role["id"]

payload = json.dumps({
    "accessKeyExpiration":sats,
    "accessKeyName":"miles-access-key-87",
    "defaultRoleId":service_account_role_id, # Use a function to translate a role name here. It does not 'just work' with the role name. confirmed
    "enabled":True,
    "enableKeyExpiration":True,
    "timeZone":"America/Los_Angeles",
    "type":"SERVICE_ACCOUNT",
    "username":"miles-service-account-87"
})

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(f"Request Status Code: {response.status_code}")
with open("access_key.json", "w") as access_key:
    access_key.write(response.text)
