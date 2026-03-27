#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/sbom-dependencies/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import json
from apu.utils import (
    login,
    http_logging,
    constants
)  # importing this should trigger the login procedure

# http_logging.http_logging()

def list(role):
    url = f"{login.settings['url']}/user/role"
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    return json.loads(response.text)

    # files.list_to_csv(file_name, json_role)

def update_user(user, user_dict=None):
    if user_dict:
        user.update(user_dict)
    pc_api.user_update(user)
    return user
