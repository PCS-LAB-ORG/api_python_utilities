#!/bin/bash python

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import json
import pprint
import os, sys
import requests

from prismacloud.api import pc_api

from apu.utils import login, http_logging # importing this should trigger the login procedure

http_logging.http_logging()

# https://pan.dev/prisma-cloud/api/code/get-vcs-repository-page/
def get_vcs_repository_page(data=''):
    url = f"{login.settings['url']}/code/api/v1/vcs-repository/repositories"
    response = requests.request("POST", url, headers=login.headers, data=data)
    response.raise_for_status()
    repository_list = json.loads(response.text)
    for repo in repository_list:
        pprint.pprint(repo)
    return repository_list

if __name__ == "__main__":
    get_vcs_repository_page()
