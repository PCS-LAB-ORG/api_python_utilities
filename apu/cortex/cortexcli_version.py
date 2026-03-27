import json
import pprint

import requests
from requests.exceptions import HTTPError
from apu.cortex import login

domain, headers = login.login()

url = f"{domain}/public_api/v1/unified-cli/releases/version"

response = requests.get(url, headers=headers)
try:
    response.raise_for_status()
    js_res = json.loads(response.text)
    pprint.pprint(js_res)
except HTTPError as e:
    print(e)
