#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/sbom-dependencies/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import json
import requests
from prismacloud.api import pc_api

from apu.utils import login # importing this should trigger the login procedure

def list(role=None):
    url = f"{login.settings['url']}/user/role"

    response = requests.request("GET", url, headers=login.headers)
    response.raise_for_status()
    role_list = json.loads(response.text)
    if not role:
        return role_list
    else:
        for r in role_list:
            if role.get("name") == r.get("name"):
                return r
    # files.list_to_csv(file_name, json_role)

def update_user(user, user_dict=None):
    if user_dict:
        user.update(user_dict)
    pc_api.user_update(user)
    return user
