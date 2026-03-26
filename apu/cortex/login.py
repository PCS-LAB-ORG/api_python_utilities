import sys
import os
import requests
import json
import pprint
from dotenv import dotenv_values
from pathlib import Path

def login():
    config = dotenv_values(f"{Path.home()}/.cortexcloud/lab.py")
    domain = config.get('CORTEX_DOMAIN')
    headers = {
        "Authorization": config.get("CORTEX_API_KEY"),
        "x-xdr-auth-id": config.get("CORTEX_API_KEY_ID"),
        "Accept-Encoding": "",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    return domain, headers