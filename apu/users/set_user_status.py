#!/bin/bash python

'''
Set user status enabled/disabled.
https://pan.dev/prisma-cloud/api/cspm/update-user-profile/
https://live.paloaltonetworks.com/t5/general-topics/disable-user/td-p/207822

This script receives 200 code even if the status is unchanged.
'''
# WARNING this username field supports regex. I'd recommend always being very explicit or searching for users 
# with the same string.
username = "" # Use to toggle status. Documented as email but, username handles service accounts and users
enable = "false"

import requests
import os, sys

from prismacloud.api import pc_api

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

  # # You must initialize logging, otherwise you'll not see debug output.
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  requests_log = logging.getLogger("requests.packages.urllib3")
  requests_log.setLevel(logging.DEBUG)
  requests_log.propagate = True
# http_logging()

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": DOMAIN,
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}
# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

url = f"{settings["url"]}/user/{username}/status/{enable}"

pc_api.configure(settings=settings)

payload = {}
headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': '*/*',
  'x-redlock-auth': pc_api.token,
}

response = requests.request("PATCH", url, headers=headers, data=payload)
response.raise_for_status()
print(response)