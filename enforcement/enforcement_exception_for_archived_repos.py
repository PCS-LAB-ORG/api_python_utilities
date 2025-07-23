#!/bin/bash python

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import json
import sys, os
import requests

from prismacloud.api import pc_api


sys.path.append(os.path.abspath(f"."))
from creds_lab import PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY, DOMAIN


def http_logging():
    #############################################################################################
    # This section would turn on extra logging for http requests
    #############################################################################################
    import logging

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    ####################################################################################
# http_logging()

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": DOMAIN,
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}

# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

pc_api.configure(settings=settings)

pc_api.debug = True

payload = ""

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*",
    "x-redlock-auth": pc_api.token,
}


# https://pan.dev/prisma-cloud/api/code/get-vcs-repository-page/
def get_vcs_repository_page():
    # payload = json.dumps({"filters": {"archived": ["true"]}})
    print("post get_vcs_repository_page")
    url = f"{settings['url']}/code/api/v1/vcs-repository/repositories"
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
    repository_list = json.loads(response.text)
    id_name = []
    for repo in repository_list:
        if repo["isArchived"] is True:
            print(f"{repo['id']} {repo['fullName']}")
            id_name.append({"accountId": repo["id"], "accountName": repo["fullName"]})
    return id_name


# https://pan.dev/prisma-cloud/api/code/add-rule/
def add_rule(archived_repo_id_name):
    # Create/update an enforcement rule exception to set all archived repos to OFF for all categories
    # 'id' and 'fullName' are needed from the vcs call

    url = f"{settings['url']}/code/api/v1/enforcement-rules"

    payload = json.dumps(
        {
            "codeCategories": {
                "IAC": {
                    "commentsBotThreshold": "OFF",
                    "hardFailThreshold": "OFF",
                    "softFailThreshold": "OFF",
                },
                "LICENSES": {
                    "commentsBotThreshold": "OFF",
                    "hardFailThreshold": "OFF",
                    "softFailThreshold": "OFF",
                },
                "VULNERABILITIES": {
                    "commentsBotThreshold": "OFF",
                    "hardFailThreshold": "OFF",
                    "softFailThreshold": "OFF",
                },
                "WEAKNESSES": {
                    "commentsBotThreshold": "OFF",
                    "hardFailThreshold": "OFF",
                    "softFailThreshold": "OFF",
                },
                "SECRETS": {
                    "commentsBotThreshold": "OFF",
                    "hardFailThreshold": "OFF",
                    "softFailThreshold": "OFF",
                },
            },
            "name": "Archived Repo Exception3",
            "repositories": archived_repo_id_name,
        }
    )
    # print(payload)
    # exit
    # http_logging()
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
    print(response.text)


archived_repo_id_name = get_vcs_repository_page()

# Create a manual list
# quit()
print(archived_repo_id_name)
print()
print()
add_rule(archived_repo_id_name)
