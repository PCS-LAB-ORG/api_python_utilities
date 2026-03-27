#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/get-tags/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import json

import requests

from apu.utils import login # importing this should trigger the login procedure

def get_tags():
    payload = ""
    url = f"{login.settings['url']}/code/api/v1/tag-rules"
    response = requests.request("GET", url, headers=login.headers, data=payload)
    response.raise_for_status()
    tag_list = json.loads(response.text)
    # pprint.pprint(tag_list)
    return tag_list
