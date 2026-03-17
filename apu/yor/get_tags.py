#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/get-tags/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os, sys
import json
import pprint
import requests

from prismacloud.api import pc_api

user_home = os.environ.get("HOME")
with open(f"{user_home}/.prismacloud/credentials.json", 'r') as creds:
    creds_json = json.load(creds)[0]
    print(creds_json)
    DOMAIN = creds_json["url"]
    PRISMA_ACCESS_KEY = creds_json["identity"]
    PRISMA_SECRET_KEY = creds_json["secret"]

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": DOMAIN,
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}
# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

pc_api.configure(settings=settings)

pc_api.debug = True

payload = ''
headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': '*/*',
  'x-redlock-auth': pc_api.token
}

url = f"{settings['url']}/code/api/v1/tag-rules"
response = requests.request("GET", url, headers=headers, data=payload)
response.raise_for_status()
pprint.pprint(json.loads(response.text))
