#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/get-bom-report/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os
import json
import pprint
import requests


def http_logging():
    #############################################################################################
    # This section would turn on extra logging for http requests
    #############################################################################################
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
    ####################################################################################
# http_logging()

from prismacloud.api import pc_api

user_home = os.environ.get("HOME")
with open(f"{user_home}/.prismacloud/credentials.json", 'r') as creds:
    creds_json = json.load(creds)[0]
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
pc_api.debug = False

pc_api.configure(settings=settings)

payload = ''

format = "cyclonedx"
material = "oss"

headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': '*/*',
  'x-redlock-auth': pc_api.token
}

repository_id = ""

url = f"{settings['url']}/bridgecrew/api/v1/bom/getBOMReport/{repository_id}?format={format}&material={material}"
response = requests.request("GET", url, headers=headers, data=payload)
response.raise_for_status()
js_res = json.loads(response.text)
pprint.pprint(js_res)
