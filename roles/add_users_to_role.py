#!/bin/bash python
# https://pan.dev/prisma-cloud/api/cspm/update-profile-v-2/
# https://github.com/PaloAltoNetworks/prismacloud-api-python/blob/e43d02ed929a013140bcbbe2488a4cfa8479cbfb/prismacloud/api/cspm/_endpoints.py#L215

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import pprint, sys, os
from datetime import datetime

from prismacloud.api import pc_api

## LOGIN Portion
# These 3 lines will put the directory of the script onto 
# the path and read a file called creds.py and that holds 
# my credentials in property file format which is also 
# valid python code.
sys.path.append(os.path.abspath(f"."))
from creds_lab import PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": "https://api.ca.prismacloud.io/",
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}

pc_api.configure(settings=settings)

# pc_api.debug = True

# print("\nAt this point you have an active token")
# print(pc_api.token)

with open("file.txt", "r") as file:
    user_list = file.readlines()  # Print the line without adding an extra newline

# user_name = "jumiles@paloaltonetworks.com"

print(f"\nPrisma Cloud API Get User List:\nID: {len(user_list)}\n")
for user_name in user_list:
    user = pc_api.user_read(user_name)
    pprint.pprint(user)

    print("Attempting to update user...\n")

    user.roleIds += "testrole"
    pc_api.user_update(user)

    # Final state of the role
    pprint.pprint(pc_api.user_read(user_name))