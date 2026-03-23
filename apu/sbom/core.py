#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/sbom-dependencies/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os
import json
import pprint
import requests
import xml.etree.ElementTree as etree

from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()

def dependencies(filters=None):
    if not filters:
        filters = {
            "filters": {
                "severity": ["low", "medium", "high", "critical"]
            }
        }
        only_vulnerable = False
        if only_vulnerable:
            filters['filters']['severity'] = ["low", "medium", "high", "critical"]
    payload = json.dumps(filters)

    limit = 50
    page = 0
    res_count = limit
    dependencies = []
    while res_count is limit:
        url = f"{login.cspm_session.api_url}/bridgecrew/api/v1/sbom/dependencies?page={page}&limit={limit}"
        response = requests.request("POST", url, headers=login.headers, data=payload)
        response.raise_for_status()
        js_res = json.loads(response.text)
        dependencies.extend(js_res)
        res_count = len(js_res)
        page += 1
        # pprint.pprint(js_res)
        for res in js_res:
            # print(res)
            if "packageMetadata" in res:
                print(f"Repo {res['packageMetadata']['repositoryUrl']}")
            # break
    print(f"Found {len(dependencies)} dependencies")
    return dependencies

def sbom():
    
    payload = ""

    format = "cyclonedx"
    material = "all"

    repository_id = ""

    url = f"{login.settings['url']}/bridgecrew/api/v1/bom/getBOMReport/{repository_id}?format={format}&material={material}"
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
        with open(f"logs/{filename}", "w") as file:
            # The contexts can be written directly but, this will format and indent XML
            root = etree.fromstring(res.text)
            etree.indent(root)
            file.writelines(etree.tostring(root, encoding="unicode"))

def get_filters():
    
    url = f"{login.cspm_session.api_url}/bridgecrew/api/v1/sbom/filters"

    payload = {}
    response = requests.request("GET", url, headers=login.headers, data=payload, allow_redirects=True)
    response.raise_for_status()
    filters = json.loads(response.text)
    return filters
