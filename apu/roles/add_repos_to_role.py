#!python
# https://pan.dev/prisma-cloud/api/cspm/update-user-role/
# https://github.com/PaloAltoNetworks/prismacloud-api-python/blob/e43d02ed929a013140bcbbe2488a4cfa8479cbfb/prismacloud/api/cspm/_endpoints.py#L240

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api

import csv
import json
import pprint, sys, os
from pathlib import Path
import requests
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

from apu.utils import login

current_repository_list = None
current_role_list = None

def read_repo_list_file(list_of_repos_file_name):
    with open(list_of_repos_file_name, "r+") as file:
        input_file = file.readlines()  # Print the line without adding an extra newline
    return file_contents

def get_repo_hash(file_contents):
    repo_hash = dict()
    for requested_repo in input_file:
        repo_hash[requested_repo.strip()] = ""
    return repo_hash

def match_repos_from_file_to_prisma_repos(old_list_list):
    # This matches on the repo URL
    repo_hash = {}
    global current_repository_list
    if not current_repository_list:
        current_repository_list = pc_api.repositories_list_read()
    # repo_not_found = []
    for repo in current_repository_list:
        full_name = f"{repo['owner']}/{repo['repository']}"
        # if 'url' in repo and repo['url'] in old_list_list:
        #     repo_hash[repo['url']] = repo["id"]
        # el
        if full_name in old_list_list:
            repo_hash[full_name] = repo['id']
        # else:
        #     if not "Y" == input(f"ERROR: Repository mapping not found: {repo}\n\nNo Updates have been made. Continue with found entries? (Y) "):
        #         quit()

    repo_array = list(repo_hash.values())
    return repo_array

def get_role_by_name(user_role_name):
    print(f"Prisma Cloud API Get Role: {user_role_name}")
    global current_role_list
    if not current_role_list:
        current_role_list = pc_api.user_role_list_read()
        role_backup_file_name = f".role_backup-{now}"
        with open(f".role_backup-{now}", "w+", newline="") as role_backup_file:
            writer = csv.DictWriter(role_backup_file, fieldnames=current_role_list[0].keys())
            writer.writeheader()
            writer.writerows(current_role_list)
        print(f"Took a backup of the roles before making changes and saved to {role_backup_file_name}. \
            \nThis is not the backup file the script is restoring to... Use this to roll back if there are errors or mistakes. \
            \nThis script is not written to update other attributes of the roles than description and repositories. ")
    found = "Role not found"
    found_role = {}
    for role in current_role_list:
        if role["id"] == user_role_name:
            found = role["id"]
            print(f"Found role: {role['name']}")
            found_role = role
            break
    role = found_role
    if role is {}:
        quit(f"Role not found. {user_role_name}")
    return role

def add_repos_to_role(role, repo_array):
    # codeRepositories = role["codeRepositories"]
    codeRepositoryIds = role["codeRepositoryIds"]
    # print(f"Role repositories before add: {codeRepositories}: {codeRepositoryIds}\n")

    # I left some logic that should allow for add or replace
    fun = "add" # input("'add' or 'replace' existing repos associated with role? ")
    if fun == "add":
        repo_array += codeRepositoryIds
    # elif fun == "replace":
    #     pass
    # else:
    #     quit(f"Invalid Input: {fun}")

    # make array values unique
    repo_array = list(set(repo_array))
    # Uncomment other parts of the role to overwrite the existing values
    
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
        # "description": f"Today is {now}", # This is a good way to test updates
        #   "name": user_role_name,
        # "resourceListIds": [
        #   "string"
        # ],
        # "restrictDismissalAccess": True,
        # "roleType": "string"
    }
    return user_role_update

def role_changes(role, repo_array) -> bool:
    ''' When sorted do the roles contain all the same elements. Return True if they are not the same '''
    role_repo_list = role['codeRepositoryIds']
    return not sorted(role_repo_list) == sorted(repo_array)

def update_role(user_role_name, list_of_repo_names):

    # repo_hash = get_repo_hash(list_of_repo_names)
    repo_array = match_repos_from_file_to_prisma_repos(list_of_repo_names)
    role = get_role_by_name(user_role_name)
    if role_changes(role, repo_array):
        user_role_update = add_repos_to_role(role, repo_array)
        pc_api.user_role_update(role["id"], user_role_update)
        """
        I was able to confirm that this does not overwrite unspecified portions of the role definition being updated. 1/26/2026
        """


        # Final state of the role
        updated_role = pc_api.user_role_read(role["id"])
        print(f"Updated {updated_role["name"]}:{updated_role["id"]}")
    else:
        print(f"No changes in the backup state for role '{role['name']}:{role["id"]}'. Skipping...")

def read_csv_file(file_name):
    with open(file_name, "r+") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def role_url_mapper_function(old_role_list_file, old_repo_list_file):
    # Get Repo Data
    old_repo_list_file_content = read_csv_file(old_repo_list_file)

    # Match on the URL to map the old ID
    old_repo_id_map = {}
    for repo in old_repo_list_file_content:
        # if not 0 == len(repo['url']):
        #     old_repo_id_map[repo['id']] = repo['url']
        # else:
        old_repo_id_map[repo['id']] = f"{repo['owner']}/{repo['repository']}"

    # Get Role Data
    old_role_list_file_content = read_csv_file(old_role_list_file)

    # Role to new repo ID map
    role_url_mapper = {}
    for role in old_role_list_file_content:
        new_repo_id_list = []
        if not 0 == role['codeRepositoryIds'].count(','):
            for repo_id in role['codeRepositoryIds'].replace("[", "").replace("]", "").replace("'", "").split(", "):
                try:
                    new_repo_id_list.append(old_repo_id_map[repo_id]) # use the old ID to get the URL
                except KeyError as e:
                    print(e)
        role_url_mapper[role['id']] = new_repo_id_list # update the role with the new ID list
        # role_url_mapper[role['name']] = new_repo_id_list # update the role with the new ID list
    return role_url_mapper

# Map of roles with a list of their URLs
# role_file_name = "roles_2026-02-19_10-45-37.csv" # 'Backup Restore Test' role with 8 repos in it
role_file_name = "roles_2026-02-27_11-15-56.csv" # 'Backup Restore Test' role with 1 repo in it
repo_file_name = "repos_2026-02-27_11-21-47.csv"
role_url_map = role_url_mapper_function(role_file_name, repo_file_name)
for role, urls in role_url_map.items():
    # the update function takes a list of repos instead of always reading from a file
    update_role(role, urls)
    print()
print(f"Completed restoring roles.")
'''
- [x] Can the same user have two onboard two repos with the same name from difference providers github/gitlab?

- [x] What should it do if there is no match?
    - This suggests the repo is not onboarded 
    - [x] Can Prisma 'lose track' of scan data on an unmapped repository? (Checkov scan) 
        - Consider other --repo-id 's that may be used for this repo.. This may require manual review

- [x] See if owner/repository is as accuracte as using the URL?

- [x] Do not interact with a role that has no changes to it's repo list. Account for roles with no repos.

- [x] Write a readme

This will only edit the repo list and description of each role. If you want to restore all attributes of 
the roles from that time then upda the add_repos_to_role() to add the repos to the existing role definition.
'''