#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/sbom-dependencies/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os
import json
import pprint
import requests


from prismacloud.api import pc_api
from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()


payload = json.dumps({"filters": {}})

limit = 50
page = 0
res_count = limit
dependencies = []
while res_count is limit:
    url = f"{settings['url']}/bridgecrew/api/v1/sbom/dependencies?page={page}&limit={limit}"
    response = requests.request("POST", url, headers=login.headers, data=payload)
    response.raise_for_status()
    js_res = json.loads(response.text)
    dependencies.append(js_res)
    res_count = len(js_res)
    page += 1
    # pprint.pprint(js_res)
    for res in js_res:
        # print(res)
        if "packageMetadata" in res:
            print(f"Repo {res['packageMetadata']['repositoryUrl']}")
        # break
print(f"Found {len(dependencies)} dependencies")
