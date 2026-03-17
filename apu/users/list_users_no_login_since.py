#!/bin/bash python

'''
Script to collect users that have not logged in for 180 days (set days_since_login).
This will output a list of those users with their last login time or Never.
'''
days_since_login = 180

import requests
import json
import sys, os
from datetime import datetime, timedelta

from prismacloud.api import pc_api

#############################################################################################
# This section would turn on extra logging for http requests
#############################################################################################
# import logging

# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# # # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": os.environ["PRISMA_DOMAIN"],
    "identity": os.environ["PRISMA_ACCESS_KEY"],
    "secret": os.environ["PRISMA_SECRET_KEY"]
}
# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

url = f"{settings["url"]}/v3/user"

pc_api.configure(settings=settings)

payload = {}
headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': '*/*',
  'x-redlock-auth': pc_api.token,
}

response = requests.request("GET", url, headers=headers, data=payload)

user_list = json.loads(response.text)


expiring_user_list = []
import datetime
for user in user_list:
    if user["type"] == "SERVICE_ACCOUNT":
        continue
    last_login = int(str(user["lastLoginTs"])[:10])
    try:
        # print("parse from datetime")
        datetime_object = datetime.datetime.fromtimestamp(last_login)
        current_date = datetime.datetime.now()
        time_difference = current_date - datetime_object
        outdated = time_difference > timedelta(days=days_since_login)
        if outdated:
            print(f"{user["email"]}, {datetime_object}")
            expiring_user_list.append(user)
    except:
        if -1 == user["lastLoginTs"]:
            # -1 is taken to mean they've never logged in.
            print(f"{user["email"]}, Never")
        else:
            print(f"{user["email"]}, {user["lastLoginTs"]} UNHANDLED CASE")
print(f"\n{len(expiring_user_list)} users that haven't logged in in 180 days")