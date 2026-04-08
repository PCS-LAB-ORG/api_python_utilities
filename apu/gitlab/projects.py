"""
Usage: projects.py [options]

Options:
  -v, --verbose  Verbose mode.
"""

# pip install python-gitlab

import os

from pathlib import Path

from docopt import docopt
import gitlab
from gitlab.exceptions import GitlabHttpError
import urllib3

from dotenv import load_dotenv

arguments = docopt(__doc__)

if arguments["v"]:
    urllib3.disable_warnings()

# Load variables from the .env file
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
    if arguments["v"]:
        gl.enable_debug()
    print(f"Successfully connected to GitLab at {GITLAB_URL}")
except Exception as e:
    print(f"Error connecting to GitLab: {e}")
    exit()

# Retrieve the group object
try:
    # group = gl.groups.get("gitlab-org")
    group_name = "miles-cortex-demos"
    group = gl.groups.get(group_name)
except GitlabHttpError as e:
    print(f"Group {group_name} not found.")
    raise e

# List all direct subgroups
subgroups = group.subgroups.list(get_all=False)

# Iterate through the subgroups
for subgroup in subgroups:
    print(f"Subgroup Name: {subgroup.name}, ID: {subgroup.id}")

# --- Fetc# 2. Retrieve all projects/repositories
# 'get_all=True' handles pagination automatically

# Set the number of items per page (e.g., 20)
items_per_page = 20
# Start from the first page
current_page = 3
# This variable will store all projects as we collect them
all_projects = []

keep_going = True
try:
    while keep_going:
        projects_page = group.projects.list(
            iterator=False,
            include_subgroups=True,
            page=current_page,
            per_page=items_per_page,
        )

        # Append the projects from the current page to the main list
        all_projects.extend(projects_page)

        for project in projects_page:
            project.pprint()
            print(f"* Name: {project.name}, ID: {project.id}, URL: {project.web_url}")
            break

        if not len(projects_page) == 0:
            break

        # Move to the next page
        current_page += 1
        keep_going = False

    print(f"Fetched page {current_page}, total projects so far: {len(all_projects)}")

    # 3. List direct members (pagination handled automatically with get_all=True)
    members = group.members.list(get_all=False)

    # 4. Process and print user information
    print(f"Direct members of group '{group.name}':")
    for member in members:
        member.pprint()
        print(
            f"* Name: {member.name}, Username: {member.username}, Access Level: {member.access_level}"
        )
        # quit()

except gitlab.exceptions.GitlabListError as e:
    print(f"Error: {e}")

"""
get all users and groups under a top level
regex to group groups together
update procedures for adding, moving, deleting the list of groups and users.
Put all this into a format that can be send to PC APIs
"""
