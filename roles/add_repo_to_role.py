#!/bin/bash python
# https://pan.dev/prisma-cloud/api/cspm/update-user-role/
# https://github.com/PaloAltoNetworks/prismacloud-api-python/blob/e43d02ed929a013140bcbbe2488a4cfa8479cbfb/prismacloud/api/cspm/_endpoints.py#L240

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import json
import pprint, sys, os
from pathlib import Path
import requests
from datetime import datetime

from prismacloud.api import pc_api

## LOGIN Portion
# These 3 lines will put the directory of the script onto 
# the path and read a file called creds.py and that holds 
# my credentials in property file format which is also 
# valid python code.
from pathlib import Path
sys.path.append(os.path.abspath(f"."))
from creds_lab import PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY

# Settings for Prisma Cloud Enterprise Edition
settings = {
    "url": "https://api.ca.prismacloud.io/",
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}
# os.environ["PRISMA_ACCESS_KEY"] # using an environment variable

pc_api.configure(settings=settings)

# pc_api.debug = True

# print("\nAt this point you have an active token")
# print(pc_api.token)


repo_array = []
input_file = []
with open("file.txt", "r") as file:
    input_file = file.readlines()  # Print the line without adding an extra newline
print(input_file)

repo_hash = dict()
for requested_repo in input_file:
    repo_hash[requested_repo] = ""

print(repo_hash)

repo_list = pc_api.repositories_list_read()
repo_not_found = []
for repo in repo_list:
    print(repo)
    if repo["repository"] in repo_hash.keys():
        repo_hash[repo["name"]] = repo["id"]
    else:
        repo_not_found.append(repo["repository"])

# print(repo_hash.items())
repo_array = list(repo_hash.values())
print(f"Repos found: {repo_array}")

if len(repo_not_found) > 0:
    print(f"Repos not found from list: {repo_not_found}")
    input("Continue? Press enter... ")

user_role_name = "<role name>"

print(f"\nPrisma Cloud API Get Role:\nID: {user_role_name}\n")

role_list = pc_api.user_role_list_read()
found = "Role not found"
found_role = {}
for role in role_list:
    # print(f"{role["id"]} {role["name"]}")
    if role["name"] == user_role_name:
        found = "Role found..."
        pprint.pprint(role)
        found_role = role
if role is {}:
    quit("Role not found. ")
# print(f"\n{found}")

proceed = input("Proceed to add these values to role: {user_role_name}? (type Y for yes)")
if(proceed == "Y"):
    quit()

codeRepositories = role["codeRepositories"]
codeRepositoryIds = role["codeRepositoryIds"]
print(f"{codeRepositories}: {codeRepositoryIds}")

fun = input("'add' or 'replace' existing repos associated with role?")
if (fun == "add"):
    repo_array += codeRepositoryIds

# make array values unique
uniq_arr = list(set(repo_array))
repo_array = uniq_arr

print("Attempting to update role...\n")
now=datetime.now()
user_role_update = {
  # "accountGroupIds": [
  #   "string"
  # ],
  # "additionalAttributes": {
  #   "hasDefenderPermissions": True,
  #   "onlyAllowCIAccess": True,
  #   "onlyAllowComputeAccess": True
  # },
  "codeRepositoryIds": repo_array,
#   "description": f"Today is {now}",
#   "name": user_role_name,
  # "resourceListIds": [
  #   "string"
  # ],
  # "restrictDismissalAccess": True,
  # "roleType": "string"
}

input(f"Role transform:\n{user_role_update}")

pc_api.user_role_update(found_role["id"], user_role_update)

# Final state of the role
pprint.pprint(pc_api.user_role_read(found_role["id"]))