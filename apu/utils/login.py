#!/bin/bash python

"""Prisma Cloud API CLI.

Usage:
  prismacli get-alerts --api-url=<url> --access-key=<key> --secret-key=<secret> [--limit=<limit>]
  prismacli get-assets --api-url=<url> --access-key=<key> --secret-key=<secret> [--status=<status>]
  prismacli (-h | --help)
  prismacli --version

Options:
  -h --help             Show this help screen.
  --version             Show the version of the CLI.
  --api-url=<url>       The base Prisma Cloud API URL (e.g., https://api.prismacloud.io).
  --access-key=<key>    Your Prisma Cloud Access Key ID.
  --secret-key=<secret> Your Prisma Cloud Secret Key.
  --limit=<limit>       Maximum number of results to return [default: 100].
  --status=<status>     Filter assets by status.
"""

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import json
import os
from pathlib import Path
import logging

import requests

from pcpi import session_loader
from prismacloud.api import pc_api

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

settings = {}
cspm_session = {}
session_man = {}
headers = {}


def user_pass(
    debug=False,
    redlock=None,
    url="https://api2.prismacloud.io/",
    identity="",
    secret="",
):
    # Settings for Prisma Cloud Enterprise Edition
    if not url:
        url = os.environ.get("URL")
    if not identity:
        identity = os.environ.get("IDENTITY")
    if not secret:
        secret = os.environ.get("SECRET")
    settings = {"url": url, "username": identity, "password": secret}  # access key

    url = f"{url}login"

    # To generate a token, you must have an access key and include the following values in
    # the request body parameter — access key ID as the username and your secret key as the password.
    # https://pan.dev/prisma-cloud/api/cspm/app-login/

    # payload = f"{'password': '{js_creds["secret"]}', 'username': '{js_creds["identity"]}'}"
    # payload = "{\"password\": \"" + secret + "\", \"username\": \"" + identity + "\"}"
    payload = json.dumps(settings)

    global headers
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)
    js_res = json.loads(response.text)
    response.raise_for_status()

    headers.update(get_headers(redlock, js_res.token))

    return js_res


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
        logger.warning(e)
        logger.info("Using environment variables")
        DOMAIN = os.environ.get("URL", default="<URL not found>")
        PRISMA_ACCESS_KEY = os.environ.get("IDENTITY", default="<IDENTITY not found>")
        PRISMA_SECRET_KEY = os.environ.get("SECRET", default="<SECRET not found>")
        return {
            "url": DOMAIN,
            "identity": PRISMA_ACCESS_KEY,
            "secret": PRISMA_SECRET_KEY,
        }
    return settings


# TODO write in the login function to take the access/secret/url and cycle through login options.


def login(
    debug=False,
    redlock=None,
    credential_name="credentials",
    lib="pc_api",
    access_key=None,
    secret_key=None,
    url=None,
):
    """what priority order do I want to assume here?"""
    """
    Anything passed comes first.
    More local gets priority.
    Do we allow dieriving partial info when passed to the function?

    """
    if access_key and secret_key and url:
        return user_pass(
            debug=debug,
            redlock=redlock,
            url=url,
            identity=access_key,
            secret=secret_key,
        )
    elif lib == "pc_api":
        if not credential_name:
            logger.debug(
                "Credential file not given so using environment variables. Only prismacloud-api is supported."
            )
        return login_pc_api(
            debug=debug, redlock=redlock, credential_name=credential_name
        )
    elif lib == "pcpi":
        return login_pcpi(redlock=redlock, credential_name=credential_name)
    else:
        raise Exception("Unknown login library")


def login_pc_api(debug=False, redlock=None, credential_name="credentials"):

    settings = common_settings_file(credential_name=credential_name)
    pc_api.configure(settings=settings)
    if None is pc_api.token:
        raise FileNotFoundError(
            "Authentication with prismacloud.api env vars URL, IDENTITY, and SECRET failed."
        )
    pc_api.debug = debug

    global headers
    headers = get_headers(redlock, pc_api.token)
    return pc_api


def login_pcpi(redlock=None, logger=None, credential_name="credentials"):
    settings = get_settings_file_name(credential_name=credential_name)
    # https://github.com/PaloAltoNetworks/pc-python-integration
    if not logger:
        session_managers = session_loader.load_config(file_path=settings)
    else:
        session_managers = session_loader.load_config(file_path=settings, logger=logger)
    global session_man
    session_man = session_managers[0]
    global cspm_session
    cspm_session = session_man.create_cspm_session()

    global headers
    headers = get_headers(redlock=redlock, token=cspm_session.token)

    return cspm_session


def get_headers(redlock=True, token=None):

    # global redlock
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
