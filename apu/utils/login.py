#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/get-tags/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import os, sys
import json
import pprint
import requests
from pathlib import Path

from pcpi import session_loader
from prismacloud.api import pc_api

settings = {}

def user_pass(debug=False, redlock=None, url="https://api2.prismacloud.io/", identity="", secret=""):
    # Settings for Prisma Cloud Enterprise Edition

    settings = {
        "url": url,
        "identity": identity, # access key
        "secret": secret
    }

    pc_api.configure(settings=settings)
    pc_api.debug = debug

    payload = ""

    global headers
    headers = get_headers(redlock)

    # print('Prisma Cloud API Current User:')
    # print(pc_api.current_user())
    # print('Prisma Cloud Compute API Intelligence:')
    # print(pc_api.statuses_intelligence())

    # print('Prisma Cloud API Object:')
    # print(pc_api)
    return pc_api

def get_settings_file_name(credential_name="credentials"):
    return f"{Path.home()}/.prismacloud/{credential_name}.json"


def common_settings_file(credential_name="credentials"):
    with open(get_settings_file_name(credential_name=credential_name)) as creds:
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
    return settings


def login(debug=False, redlock=None, credential_name="credentials", lib="pc_api"):
    if lib == "pc_api":
        return login_pc_api(debug=False, redlock=None, credential_name="credentials")
    elif lib == "pcpi":
        return login_pc_api(debug=False, redlock=None, credential_name="credentials")
    else:
        raise ("Unknown login library")


def login_pc_api(debug=False, redlock=None, credential_name="credentials"):
    settings = common_settings_file(credential_name=credential_name)
    pc_api.configure(settings=settings)
    pc_api.debug = debug

    payload = ""

    global headers
    headers = get_headers(redlock)

    return pc_api


def login_pcpi(logger=None, credential_name="credentials"):
    file_path = get_settings_file_name(credential_name=credential_name)
    # https://github.com/PaloAltoNetworks/pc-python-integration
    if not logger:
        session_managers = session_loader.load_config(file_path=file_path)
    else:
        session_managers = session_loader.load_config(
            file_path=file_path, logger=logger
        )
    session_man = session_managers[0]
    cspm_session = session_man.create_cspm_session()
    return cspm_session


def get_headers(redlock=True, token=None):

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


def refresh_token(redlock=True):
    cspm_session = session_man.create_cspm_session()
    get_headers(redlock=redlock, token=cspm_session.token)
