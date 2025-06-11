#!/bin/bash python

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
# import logging

# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# # # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": "https://api2.prismacloud.io",
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}
# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

url = f"{settings["url"]}/user/role"

pc_api.configure(settings=settings)

payload = {}
headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': '*/*',
  'x-redlock-auth': pc_api.token,
}

response = requests.request("GET", url, headers=headers, data=payload)

json_role = json.loads(response.text)
for role in json_role:
    if(role["name"] == "Reduced Developer Role"):
        pprint.pprint(role)
