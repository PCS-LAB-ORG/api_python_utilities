#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/get-tags/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os, sys
import json
import pprint
import requests
from pathlib import Path


from prismacloud.api import pc_api

settings = {}

def login(debug=False):
  with open(f"{Path.home()}/.prismacloud/credentials.json", 'r') as creds:
      creds_json = json.load(creds)[0]
      # print(creds_json)
      DOMAIN = creds_json["url"]
      PRISMA_ACCESS_KEY = creds_json["identity"]
      PRISMA_SECRET_KEY = creds_json["secret"]

  # Settings for Prisma Cloud Enterprise Edition
  global settings
  settings = {
      "url": DOMAIN,
      "identity": PRISMA_ACCESS_KEY,
      "secret": PRISMA_SECRET_KEY
  }
  # os.environ["PRISMA_ACCESS_KEY"] # using an environment variable
  # print("Logging in...")
  pc_api.configure(settings=settings)
  # print("Successfully logged in...")
  pc_api.debug = debug

  payload = ''

  
  global headers
  headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': '*/*',
    'x-redlock-auth': pc_api.token
  }

  headers_redlock = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': '*/*',
    'x-redlock-auth': pc_api.token
  }

  headers_authorization = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': '*/*',
    'Authorization': pc_api.token
  }
  return pc_api