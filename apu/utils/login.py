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
cspm_session = {}
headers = {}

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
    headers = get_headers(redlock, pc_api.token)

    return pc_api

def get_settings_file_name(credential_name="credentials"):
    return f"{Path.home()}/.prismacloud/{credential_name}.json"


def common_settings_file(credential_name="credentials"):
    global settings
    try:
        with open(get_settings_file_name(credential_name=credential_name)) as creds:
            creds_json = json.load(creds)[0]
            settings = {
                "url": creds_json["url"],
                "identity": creds_json["identity"],
                "secret": creds_json["secret"],
            }
    except FileNotFoundError as e:
        logger.warn(e)
        logger.info("Using environment variables")
        DOMAIN = os.environ.get("URL", default="<URL not found>")
        PRISMA_ACCESS_KEY = os.environ.get("IDENTITY",  default="<IDENTITY not found>")
        PRISMA_SECRET_KEY = os.environ.get("SECRET",  default="<SECRET not found>")
        settings = {
            "url": os.environ.get("URL"),
            "identity": os.environ.get("IDENTITY"),
            "secret": os.environ.get("SECRET"),
        }
    return settings


def login(debug=False, redlock=None, credential_name="credentials", lib="pc_api"):
    if not credential_name and lib == "pc_api":
        quit("Credential file not given so using environment variables. Only prismacloud-api is supported.")
    if lib == "pc_api":
        return login_pc_api(debug=False, redlock=None, credential_name="credentials")
    elif lib == "pcpi":
        return login_pcpi(redlock=None, credential_name="credentials")
    else:
        raise ("Unknown login library")


def login_pc_api(debug=False, redlock=None, credential_name="credentials"):

    settings = common_settings_file(credential_name=credential_name)
    pc_api.configure(settings=settings)

    pc_api.debug = debug
    payload = ""

    global headers
    headers = get_headers(redlock, pc_api.token)
    return pc_api

def login_pcpi(redlock=None, logger=None, credential_name="credentials"):
    settings = get_settings_file_name(credential_name=credential_name)
    # https://github.com/PaloAltoNetworks/pc-python-integration
    if not logger:
        session_managers = session_loader.load_config(file_path=settings)
    else:
        session_managers = session_loader.load_config(
            file_path=settings, logger=logger
        )
    session_man = session_managers[0]
    global cspm_session
    cspm_session = session_man.create_cspm_session()

    global headers
    headers = get_headers(redlock=redlock, token=cspm_session.token)

    return cspm_session


def get_headers(redlock=True, token=None):

    global redlock
    if redlock:
        return {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "x-redlock-auth": token,
        }
    else:
        return {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "Authorization": token,
        }


def refresh_token(redlock=True):
    cspm_session = session_man.create_cspm_session()
    get_headers(redlock=redlock, token=cspm_session.token)
