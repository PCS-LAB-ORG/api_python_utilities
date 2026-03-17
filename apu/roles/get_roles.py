#!python

import requests
import json
import os
from datetime import datetime

from apu.utils import login

start_time = datetime.now()
file_name = f"{os.getcwd()}/roles_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.csv"


url = f"{settings['url']}/user/role"
payload = {}

response = requests.request("GET", url, headers=headers, data=payload)
response.raise_for_status()
json_role = json.loads(response.text)

files.list_to_csv(file_name, json_role)
