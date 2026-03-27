import json
import pprint

import requests
from requests.exceptions import HTTPError
from apu.cortex import login

domain, headers = login.login()

url = f"{domain}/public_api/v1/issue/search"

payload = {
    "request_data": {
        "filters": [{"field": "issue_id", "operator": "in", "value": [0]}],
        "search_from": 0,
        "search_to": 2,
        "sort": {"field": "issue_id", "keyword": "asc"},
    }
}

response = requests.post(url, json=payload, headers=headers, timeout=60)
try:
    response.raise_for_status()
    js_res = json.loads(response.text)
    pprint.pprint(js_res)
except HTTPError as e:
    if e.response.status_code == 400:
        print("Seen when table does not exist")
    print(e)
    if hasattr(e, "response"):
        print(e.response.text)
