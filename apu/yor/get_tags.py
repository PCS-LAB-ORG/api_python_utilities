#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/get-tags/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os, sys
import json
import pprint
import requests

from prismacloud.api import pc_api
from apu.utils import login, http_logging # importing this should trigger the login procedure
# http_logging.http_logging()


payload = ''

url = f"{settings['url']}/code/api/v1/tag-rules"
response = requests.request("GET", url, headers=login.headers, data=payload)
response.raise_for_status()
pprint.pprint(json.loads(response.text))
