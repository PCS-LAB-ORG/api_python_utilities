import csv
import os
from pathlib import Path

import gitlab
from gitlab.exceptions import GitlabAuthenticationError

from dotenv import load_dotenv

script_dir = Path(__file__).resolve().parent  # directory of this script

groups_filename = f"{script_dir}/groups.csv"
projects_filename = f"{script_dir}/projects.csv"
BASE_GROUP_ID = "miles-cortex-demos"
# BASE_GROUP_ID = "gitlab-org" # gitlab-org has a lot of repos and deep group levels for testing

def authenticate():
    # Load variables from the .env file in C:/Users/<username>/.gitlab/.env
    dotenv_path = f"{Path.home()}/.gitlab/.env"
    load_dotenv(dotenv_path=dotenv_path)


    # --- Configuration ---
    # Replace with your GitLab instance URL (e.g., 'https://gitlab.com')
    GITLAB_URL = os.environ.get("GITLAB_URL")
    # Replace with your Personal Access Token
    PRIVATE_TOKEN = os.environ.get("PRIVATE_TOKEN")

    # --- Initialize GitLab connection ---
    try:
        gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN, ssl_verify=False)
        gl.auth()
        print(f"Successfully connected to GitLab at {GITLAB_URL}")
        return gl
    except GitlabAuthenticationError as e:
        print(f"Error connecting to GitLab: {e}")
        raise e

def get_projects_recursive(group_id):
    try:
        group = gl.groups.get(group_id)
        all_groups.append(
            {
                "group_url": group.web_url,
                "group": group.full_name,
                "group_archived": group.archived,
                "group_id": group.id,
            }
        )

        # 2. Get subgroups of this group and recurse
        subgroups = group.subgroups.list(all=True)
        for subgroup_info in subgroups:
            # Note: subgroup_info is a GroupSubgroup object. Need to use its ID.
            get_projects_recursive(subgroup_info.id)

    except gitlab.exceptions.GitlabError as e:
        print(f"Error processing group {group_id}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_members(group):
    all_members = []
    for member in group.members.list(all=True):
        all_members.append(
            {
                "group_url": group.web_url,
                "username": member.username,
                "name": member.name,
                "locked": member.locked,
                "state": member.state,
                "group": group.full_name,
                "group_archived": group.archived,
                "group_id": member.group_id,
            }
        )

def get_projects(group):
    all_projects = []
    # 1. Get projects directly within this group

    # Set the number of items per page (e.g., 20)
    items_per_page = 20
    # Start from the first page
    current_page = 1
    keep_going = True
    while keep_going:
        projects = group.projects.list(
            iterator=False,
            include_subgroups=True,
            page=current_page,
            per_page=items_per_page,
        )
        all_projects.extend(projects)

        if not len(projects) == 0:
            break

        # Move to the next page
        current_page += 1
        keep_going = False


gl = authenticate()

all_groups = []

# Start the recursion from the base group
get_projects_recursive(BASE_GROUP_ID)
for group in all_groups:
    print(group)

# Open a new CSV file for writing
with open(groups_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = all_groups[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_groups)

all_projects = []
get_projects(BASE_GROUP_ID)
# Start the recursion from the base group
for group in all_projects:
    print(group)

# Open a new CSV file for writing
with open(projects_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = all_projects[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_projects)
