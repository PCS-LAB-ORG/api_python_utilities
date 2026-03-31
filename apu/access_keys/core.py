#!python

# Primary API Doc link
# https://pan.dev/prisma-cloud/api/cspm/get-my-access-keys/

import json
import pprint

import requests

from prismacloud.api import pc_api

from apu.utils import login  # importing this should trigger the login procedure


def get():
    # pc_api.access_keys_list_read()
    url = f"{login.settings['url']}/access_keys"
    payload = {}
    response = requests.request("GET", url, headers=login.headers, data=payload)
    response.raise_for_status()
    return json.loads(response.text)


def delete(key=None, key_id=None):
    # pc_api.access_key_delete()
    # Read access key id from script arguments
    key = key_or_id(key=key, key_id=key_id)

    url = f"{login.settings['url']}/access_keys/{key_id}"
    payload = {}
    response = requests.request("DELETE", url, headers=login.headers, data=payload)
    response.raise_for_status()
    print(f"{response.status_code} {response.text}")


def add(
    key=None,
    days_till_expiration=90,
    key_name="My Prisma Key",
    key_output_file_name="access_key.json",
):
    url = f"{login.settings['url']}/access_keys"
    if key:
        key_name = key["name"]

    sats = days_to_timestamp(days_till_expiration)
    payload = json.dumps({"expiresOn": sats, "name": key_name})

    response = requests.request("POST", url, headers=login.headers, data=payload)
    response.raise_for_status()
    js_res = json.loads(response.text)
    # pprint.pprint(js_res)
    with open(key_output_file_name, "w") as output:
        output.writelines(js_res)


def days_to_timestamp(days):
    # 1753206001977 epoch
    # 1753290980327 first request
    # 1753292246888 second request
    # 259200000
    #     future_date_utc = datetime(2026, 1, 1, 10, 30, 0) # Year, Month, Day, Hour, Minute, Second

    #  pylint: disable=import-outside-toplevel
    from datetime import datetime, timedelta

    # Get today's date
    current_datetime = datetime.now()

    # Calculate the date 90 days from today
    future_date = current_datetime + timedelta(days=days)
    # The API requires 13 characters in the timestamp so I add a single millisecond. The UI only shows down to the second. Rounding is assumed at this point unconfirmed.
    day = future_date  # datetime(2025, 6, 7, 0, 0, 0, 1)
    timestamp_float = day.timestamp()
    # timestamp_int = int(timestamp_float)
    sats = str(timestamp_float).replace(".", "")[:13]  # Get first 13 characters
    return sats


def is_expired(key=None, key_id=None):
    key = key_or_id(key, key_id)
    return key["status"] == "expired"


def key_or_id(key=None, key_id=None):
    if key:
        return key
    elif key_id:
        return pc_api.access_key_read(key_id)
    else:
        raise TypeError("key not found")


if __name__ == "__main__":
    login.login()
    key_list = list_keys()
    pprint.pprint(key_list)
