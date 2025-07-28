#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/get-bom-report/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os
import json
import pprint
import requests
import xml.etree.ElementTree as etree

from prismacloud.api import pc_api

env_keys = os.environ.keys()
if "HOME" in env_keys:
    user_home = os.environ.get("HOME")
elif "USERPROFILE" in env_keys:
    user_home = os.environ.get("USERPROFILE")
else:
    print("HOME and USERPROFILE are not found in environment variables. Assuming '.'")
    user_home = "."
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
material = "all"

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
for format in js_res["bomResponse"]:
    res = requests.request("GET", format["reportLink"], verify=False)
    res.raise_for_status()
    filename = res.headers["Content-Disposition"].removeprefix("attachment; filename = ").replace("\"", "")
    print(f"{format['format']} {filename}")
    with open(filename, "w") as file:
        # The contexts can be written directly but, this will format and indent XML
        root = etree.fromstring(res.text)
        etree.indent(root)
        file.writelines(etree.tostring(root, encoding="unicode"))
