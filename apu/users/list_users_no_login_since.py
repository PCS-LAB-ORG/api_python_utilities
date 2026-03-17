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
from apu.utils import login, http_logging # importing this should trigger the login procedure
# http_logging.http_logging()


payload = {}

response = requests.request("GET", url, headers=login.headers, data=payload)

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