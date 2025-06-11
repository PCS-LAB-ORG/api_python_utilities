#!/bin/bash python

# Primary API Doc link
# https://pan.dev/prisma-cloud/api/cspm/add-user-v-3/

import requests
import sys, os

from prismacloud.api import pc_api

sys.path.append(os.path.abspath(f".."))
from creds_lab import PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": "https://api2.prismacloud.io",
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}
# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

id = "<my username>"
id = "miles-service-account-85"

url = f"{settings["url"]}/user/{id}"

pc_api.configure(settings=settings)

payload = {}
headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': '*/*',
  'x-redlock-auth': pc_api.token,
}

response = requests.request("DELETE", url, headers=headers, data=payload)
response.raise_for_status()
print(response)