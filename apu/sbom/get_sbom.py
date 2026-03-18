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
from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()


payload = ""

format = "cyclonedx"
material = "all"

repository_id = ""

url = f"{settings['url']}/bridgecrew/api/v1/bom/getBOMReport/{repository_id}?format={format}&material={material}"
response = requests.request("GET", url, headers=login.headers, data=payload)
response.raise_for_status()
js_res = json.loads(response.text)
for format in js_res["bomResponse"]:
    res = requests.request("GET", format["reportLink"], verify=False)
    res.raise_for_status()
    filename = (
        res.headers["Content-Disposition"]
        .removeprefix("attachment; filename = ")
        .replace('"', "")
    )
    print(f"{format['format']} {filename}")
    with open(filename, "w") as file:
        # The contexts can be written directly but, this will format and indent XML
        root = etree.fromstring(res.text)
        etree.indent(root)
        file.writelines(etree.tostring(root, encoding="unicode"))
