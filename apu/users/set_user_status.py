#!/bin/bash python

"""
Set user status enabled/disabled.
https://pan.dev/prisma-cloud/api/cspm/update-user-profile/
https://live.paloaltonetworks.com/t5/general-topics/disable-user/td-p/207822

This script receives 200 code even if the status is unchanged.
"""
# WARNING this username field supports regex. I'd recommend always being very explicit or searching for users
# with the same string.
username = ""  # Use to toggle status. Documented as email but, username handles service accounts and users
enable = "false"

import requests
import os, sys

from prismacloud.api import pc_api
from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure

# http_logging.http_logging()

url = f"{login.settings["url"]}/user/{username}/status/{enable}"


payload = {}

response = requests.request("PATCH", url, headers=login.headers, data=payload)
response.raise_for_status()
print(response)
