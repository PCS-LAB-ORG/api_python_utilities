#!/bin/bash python

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import json
import pprint
import requests

from apu.utils import (
    login,
    http_logging,
)  # importing this should trigger the login procedure


# https://pan.dev/prisma-cloud/api/code/get-vcs-repository-page/
def get_vcs_repository_page(data=""):
    url = f"{login.settings['url']}/code/api/v1/vcs-repository/repositories"
    response = requests.request("POST", url, headers=login.headers, data=data)
    response.raise_for_status()
    repository_list = json.loads(response.text)
    for repo in repository_list:
        pprint.pprint(repo)
    return repository_list


def get_repositories(includeUnmappedProjects=False, repo_search_list=[]):
    payload = ""
    params = {"includeUnmappedProjects": includeUnmappedProjects}
    url = f"{login.settings['url']}/code/api/v1/repositories"
    response = requests.request("GET", url, headers=login.headers, params=params)
    response.raise_for_status()
    repository_list = json.loads(response.text)
    
    repository_match_list_non_onboarded = []
    source_id_list = [repo['Source ID'] for repo in repo_search_list]
    for repo in repository_list:
        if len(source_id_list) == 0 or f"{repo['owner']}/{repo['repository']}" in source_id_list:
            repository_match_list_non_onboarded.append(repo)
    return repository_match_list_non_onboarded


if __name__ == "__main__":
    login.login()
    get_vcs_repository_page()
