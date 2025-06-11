#!/bin/bash python
# https://pan.dev/prisma-cloud/api/cspm/add-user-v-2/
# https://github.com/PaloAltoNetworks/prismacloud-api-python/blob/e43d02ed929a013140bcbbe2488a4cfa8479cbfb/prismacloud/api/cspm/_endpoints.py#L215

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import sys, os, json, csv

from prismacloud.api import pc_api

## LOGIN Portion
# These 3 lines will put the directory of the script onto 
# the path and read a file called creds.py and that holds 
# my credentials in property file format which is also 
# valid python code.
sys.path.append(os.path.abspath(f"."))
from creds_lab import DOMAIN, PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": DOMAIN,
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}

pc_api.configure(settings=settings)

# pc_api.debug = True

# print("\nAt this point you have an active token")
# print(pc_api.token)

# All required except 'activeRole' and 'accessKeysAllowed' (access keys allowed by default) 
def create_user(user):
    payload = json.dumps({
    "accessKeysAllowed": True,
    "activeRole": {},
    "defaultRoleId": user["defaultRoleId"],
    "email": user["email"],
    "firstName": user["firstName"],
    "lastName": user["lastName"],
    "roleIds": user["roleIds"].replace(" ", ", "),
    "timeZone": user["timeZone"]
    })
    res = pc_api.user_create(payload)
    print(f"Create User ({user["email"]}) response code: {res}")

with open("user_list.csv", "r") as user_list:
    csv_user_list = csv.DictReader(user_list)
    for user in csv_user_list:
        create_user(user)
