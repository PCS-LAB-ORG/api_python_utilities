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


def login(debug=False, redlock=None):
    with open(f"{Path.home()}/.prismacloud/credentials.json") as creds:
        creds_json = json.load(creds)[0]
        DOMAIN = creds_json["url"]
        PRISMA_ACCESS_KEY = creds_json["identity"]
        PRISMA_SECRET_KEY = creds_json["secret"]

    # Settings for Prisma Cloud Enterprise Edition
    global settings
    settings = {
        "url": DOMAIN,
        "identity": PRISMA_ACCESS_KEY,
        "secret": PRISMA_SECRET_KEY,
    }
    pc_api.configure(settings=settings)
    pc_api.debug = debug

    payload = ""

    global headers
    headers = get_headers(redlock)

    return pc_api


def get_headers(redlock=True):

    global headers
    if redlock:
        return {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "x-redlock-auth": pc_api.token,
        }
    else:
        return {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "Authorization": pc_api.token,
        }
