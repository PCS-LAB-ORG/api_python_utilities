#!/bin/bash python
# https://pan.dev/prisma-cloud/api/cspm/add-user-v-2/
# https://github.com/PaloAltoNetworks/prismacloud-api-python/blob/e43d02ed929a013140bcbbe2488a4cfa8479cbfb/prismacloud/api/cspm/_endpoints.py#L215

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import sys, os, json, csv


from prismacloud.api import pc_api
from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()


# All required except 'activeRole' and 'accessKeysAllowed' (access keys allowed by default)
def create_user(user):
    payload = json.dumps(
        {
            "accessKeysAllowed": True,
            "activeRole": {},
            "defaultRoleId": user["defaultRoleId"],
            "email": user["email"],
            "firstName": user["firstName"],
            "lastName": user["lastName"],
            "roleIds": user["roleIds"].replace(" ", ", "),
            "timeZone": user["timeZone"],
        }
    )
    res = pc_api.user_create(payload)
    print(f"Create User ({user["email"]}) response code: {res}")


with open("user_list.csv") as user_list:
    csv_user_list = csv.DictReader(user_list)
    for user in csv_user_list:
        create_user(user)
