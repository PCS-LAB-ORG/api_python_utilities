#!/bin/bash python
# https://pan.dev/prisma-cloud/api/cspm/update-profile-v-2/
# https://github.com/PaloAltoNetworks/prismacloud-api-python/blob/e43d02ed929a013140bcbbe2488a4cfa8479cbfb/prismacloud/api/cspm/_endpoints.py#L215

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import pprint


from prismacloud.api import pc_api
from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()

with open("file.txt") as file:
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
