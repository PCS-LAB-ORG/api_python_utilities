#!python

# https://pan.dev/prisma-cloud/api/cspm/get-features/

import json
import pprint
from dataclasses import dataclass
from dacite import from_dict
import requests
from apu.utils import login


@dataclass
class features:
    feat: list[str]


def get():
    payload = ""

    url = f"{login.settings['url']}/authz/v1/feature"
    response = requests.request(
        method="GET", url=url, headers=login.headers, data=payload
    )
    response.raise_for_status()
    return json.loads(response.text)


def json_to_object(data=None):
    return from_dict(
        data_class=features,
        data=data,
    )


if __name__ == "__main__":
    login.login()
    features_obj = get()
    pprint.pprint(features_obj)
