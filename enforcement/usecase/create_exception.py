#!python

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import json
import os
import requests
import csv
import argparse
from prismacloud.api import pc_api

parser = argparse.ArgumentParser(description='''
Prerequisite steps:
Python 3.11. 3.6-3.12 are expected to work.
Python libraries required: requests, prismacloud-api, argparse

Run the script
python create_exception.py <args>
''',
epilog='''
Core Use Cases
1. Get list of archived repos as a local csv
2. Create new exceptions with list of archived repos
3. Create new exception with edited local list of repos
4. Update existing exception with local list of repos
5. Update existing exception with a repo that already exists in a different exception
6. Show that argparse can be used instead of hardcoding values. 
7. Show help statement
8. Show README.md
''', formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--file", required=True, help="Relative file path csv formatted set of repositories containing at least 'id' and 'fullName'. The file created will have this format.")
parser.add_argument("--exception_name", required=False, help="The name of the exception that you are creating or updating. Without this it will ask to write repos to a local file --file")
parser.add_argument("--force", action='store_true', default=False, help="Automatically accept all prompts.")
parser.add_argument("--exception_definition_file", help="Unimplemented. Currently the codeCategories flags are hardcoded as variable 'exception_definition'.")
parser.add_argument(
    "--PRISMA_DOMAIN",
    default=os.environ.get("PRISMA_DOMAIN"),
    required=False,
    help="like https://api.ca.prismacloud.io for Canada. Default environment variable PRISMA_DOMAIN",
)
parser.add_argument(
    "--PRISMA_ACCESS_KEY",
    default=os.environ.get("PRISMA_ACCESS_KEY"),
    required=False,
    help="Default environment variable PRISMA_ACCESS_KEY",
)
parser.add_argument(
    "--PRISMA_SECRET_KEY",
    default=os.environ.get("PRISMA_SECRET_KEY"),
    required=False,
    help="Default environment variable PRISMA_SECRET_KEY",
)
args = parser.parse_args()

if not (args.PRISMA_DOMAIN or args.PRISMA_ACCESS_KEY or args.PRISMA_SECRET_KEY):
    quit("Unable to authenticate without domain, access, and secret keys")

'''
How to edit this exception definition.
Code Categories: These are related to enabled features in Prisma.
*Threshold values: enumeration of OFF, INFO, LOW, MEDIUM, HIGH, CRITICAL
Some category threshold levels are not supported. Please see documentation 
or review what is allowed in your tenant.
https://docs.prismacloud.io/en/enterprise-edition/content-collections/application-security/risk-management/monitor-and-manage-code-build/enforcement
'''
exception_definition = {
    "codeCategories": {
        "BUILD_INTEGRITY": {
            "softFailThreshold": "OFF",
            "hardFailThreshold": "OFF",
            "commentsBotThreshold": "OFF"
        },
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
    }
}

# import sys, os
# sys.path.append(os.path.abspath(f"../../creds")) # relative to file
# sys.path.append(os.path.abspath(f"creds")) # relative to repo root
# from creds_lab import PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY, PRISMA_DOMAIN

settings = {
    "url": args.PRISMA_DOMAIN,
    "identity": args.PRISMA_ACCESS_KEY,
    "secret": args.PRISMA_SECRET_KEY
}

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

pc_api.configure(settings=settings)
pc_api.debug = True

payload = ""
headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "*/*",
    "x-redlock-auth": pc_api.token,
}

def flatten_json(nested_json):
    """
    Flattens a nested JSON object into a single-level dictionary.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


# https://pan.dev/prisma-cloud/api/code/get-vcs-repository-page/
def get_vcs_repository_page(local_file):
    payload = json.dumps({"filters": {"archived": ["true"]}})
    print("post get_vcs_repository_page")
    url = f"{settings['url']}/code/api/v1/vcs-repository/repositories"
    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
    repository_list = json.loads(response.text)
    key_list = set()
    repo_list = []
    for repo in repository_list:
        flat_repo = flatten_json(repo)
        key_list.update(flat_repo.keys())
        repo_list.append(flat_repo)
    
    key_list = list(key_list)
    key_list.sort()
    # These are the user friendly keys I want at the beginning
    key_list.remove("isArchived")
    key_list.insert(0, "isArchived")
    key_list.remove("url")
    key_list.insert(0, "url")

    # if local file exists
    #   overwrite ?
    #       write file
    #       quit() since local = remote
    #   else
    #       proceed without writing
    # else
    #   write file
    #   quit() since local = remote
    if os.path.exists(local_file):
        overwrite = input(f"Overwrite local repo list {local_filename}\n(y) >>> ")
        if overwrite == "y":
            with open(local_filename, "w", newline="") as local_file:
                writer = csv.DictWriter(f=local_file, fieldnames=key_list)
                writer.writeheader()
                writer.writerows(repo_list)
            print("Quitting since the newly written file is the same as the remote state.")
            quit()
        print(f"Local repo list file exists as file {local_filename} and will be used to compare current exception rule state.")
        return repo_list, key_list
    else:
        print(f"local repo list does not exist. Writing now to {local_filename}")
        with open(local_filename, "w", newline="") as local_file:
            writer = csv.DictWriter(f=local_file, fieldnames=key_list)
            writer.writeheader()
            writer.writerows(repo_list)
        print("Quitting since the newly written file is the same as the remote state.")
        quit()
        
def read_local_repo_list():
    repositories = []
    with open(local_filename, "r", newline='') as repo_list:
        csv_list = csv.DictReader(repo_list)
        for repo in csv_list:
            repositories.append(repo)
        return repositories
# read_local_repo_list()

def compare_local(local_file):
    
    remote, k = get_vcs_repository_page(local_file)
    remote_url_set = set()
    print("remote repos")
    for r in remote:
        print(r["url"])
        remote_url_set.add(r["url"])

    print("")
    local = read_local_repo_list()
    local_url_set = set()
    print("local repos")
    for l in local:
        print(l["url"])
        local_url_set.add(l["url"])

    remote_only = remote_url_set - local_url_set
    print(f"remote only: {remote_only} 'set()' means empty list")

    local_only = local_url_set - remote_url_set
    print(f"local only: {local_only} 'set()' means empty list")

    if len(remote_only) == 0 and len(local_only) == 0:
        return True
    if len(remote_only) > 0:
        print("Remote repo list contains archived repos not in local list")
    if len(local_only) > 0:
        print("Local repo list contains archived repos not in remote list")
    return False
# print(compare_local())


def get_enforcement_rules():
    url = f"{settings['url']}/code/api/v1/enforcement-rules"
    payload = ''
    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    # rule_id_list = []
    return json.loads(response.text)

# https://pan.dev/prisma-cloud/api/code/add-rule/
def add_rule(archived_repo_id_name, matching_name_id):
    # Create/update an enforcement rule exception to set all archived repos to OFF for all categories
    # 'id' and 'fullName' are needed from the vcs call
    url = f"{settings['url']}/code/api/v1/enforcement-rules"

    exception_definition["name"] = exception_name
    exception_definition["repositories"] = archived_repo_id_name

    # This section handles create and updated determined by if the matching_name_id
    # exists already.
    request_method = "POST"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "*/*",
        'Authorization': pc_api.token
    }
    # https://pan.dev/prisma-cloud/api/code/edit-rule/
    if matching_name_id != "":
        exception_definition["id"] = matching_name_id
        request_method = "PUT"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "x-redlock-auth": pc_api.token, # Can I use the Authorization header for both calls? 
        }
    payload = json.dumps(exception_definition)
    http_logging()
    # url = f"{settings['url']}/bridgecrew/api/v1/enforcement-rules"
    response = requests.request(request_method, url, headers=headers, data=payload)
    response.raise_for_status()
    print(response.text)

if args.exception_name:
    exception_name = args.exception_name # "Archived Repo Exception4"
if args.file:
    local_filename = args.file # "excluded_repos2.csv"

if compare_local(local_filename):
    print("There are no differences between the local file and the repo list in Prisma.")

'''
This is the point at which we go from collecting a repo list to applying an exception to it. 
'''

if not args.exception_name:
    quit("No exception name given so this can only write the record of repositories.")

c = ""
# Handle the force flag
if args.force and args.force is True:
    c = "y"
else:
    c = input("Ready to create exception?\n(y)>>> ")

# if either case passes
if c == "y":
    remote_enforcement_rule_list = get_enforcement_rules()
    matching_name_id = "" # Blank implies the rule does not exist
    matching_rule = {}
    local_repo_list = read_local_repo_list()
    repos_in_local_list = set()
    for repo in local_repo_list:
        repos_in_local_list.add(repo["fullName"])

    for remote_rule in remote_enforcement_rule_list["rules"]:
        if exception_name == remote_rule["name"]:
            print("Matching exception found")
            print(remote_rule)
            matching_name_id = remote_rule["id"]
            matching_rule = remote_rule
        else:
            # This isn't the prettiest code but, I prefer easy to follow logic 
            # This if statement makes a single list of items that exist in both lists
            # then checks if any are found. When the API call is made there is an ambiguous 
            # error code if you try to create or update an exception with a repo that 
            # another exception already has. 
            rule_repo_list = set()
            for repo in remote_rule["repositories"]:
                rule_repo_list.add(repo["accountName"])

            if len(list(rule_repo_list.intersection(repos_in_local_list))) > 0:
                quit(f"Repos being added to rule already belong to an exception that exists. This will cause an API error code: {remote_rule}")

    repo_id_and_name_list = []
    for repo in local_repo_list:
        repo_id_and_name_list.append({"accountId": repo["id"], "accountName": repo["fullName"]})
    add_rule(repo_id_and_name_list, matching_name_id)
