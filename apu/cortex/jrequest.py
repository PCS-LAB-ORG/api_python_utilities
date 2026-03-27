import json

import requests
from requests.exceptions import HTTPError
from apu.cortex import login

domain, headers = login.login()

def post(url, payload):
    url = f"{domain}/public_api/v1/{url}"
    response = requests.post(url, json=payload, headers=headers)
    try:
        response.raise_for_status()
        res_js = json.loads(response.text)
        return res_js
    except HTTPError as e:
        print(e)
        if e.response.status_code == 403:
            js_res = json.loads(e.response.text)
            print(js_res)
            print("Probably don't have the right permissions on these creds")
        raise e

def get(url):
    url = f"{domain}/public_api/v1/{url}"
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
        res_js = json.loads(response.text)
        return res_js
    except HTTPError as e:
        print(e)
        if e.response.status_code == 403:
            js_res = json.loads(e.response.text)
            print(js_res)
            print("Probably don't have the right permissions on these creds")
        raise e
