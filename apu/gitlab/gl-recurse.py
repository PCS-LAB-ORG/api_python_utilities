# https://python-gitlab.readthedocs.io/en/stable/index.html

import csv
import os
from datetime import datetime as dt
from pathlib import Path

# pip install python-gitlab
import gitlab
import gitlab.exceptions
from gitlab.exceptions import GitlabAuthenticationError

# pip install python-dotenv
from dotenv import load_dotenv

script_dir = f"{Path(__file__).resolve().parent}/logs"  # directory of this script
os.makedirs(script_dir, exist_ok=True)


date_time_format_w_seconds = "%Y-%m-%d_%H-%M-%S"
now = dt.now().strftime(date_time_format_w_seconds)


def authenticate():

    # dotenv_path = f"{script_dir}/.env"  # Load variables from the .env file in the directory of this script
    dotenv_path = f"{Path.home()}/.gitlab/.env"  # Load variables from the .env file in C:/Users/<username>/.gitlab/.env
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


def get_groups(all_group_objects):
    """https://python-gitlab.readthedocs.io/en/stable/gl_objects/groups.html"""
    all_groups = []
    for group in all_group_objects:
        all_groups.append(
            {
                "url": group.web_url,
                "name": group.full_path,
                "archived": group.archived,
                "id": group.id,
                "ldap_access": group.ldap_access,
                "ldap_cn": group.ldap_cn,
            }
        )
    return all_groups


def get_members():
    all_members = []
    for member in list(gl.users.list(get_all=True)):
        all_members.append(
            {
                "name": member.name,
                "username": member.username,
                "locked": member.locked,
                "state": member.state,
                "id": member.id,
            }
        )
    return all_members


def get_members_by_group(group_list):
    ACCESS_LEVELS = {
        10: "GUEST_ACCESS",
        20: "REPORTER_ACCESS",
        30: "DEVELOPER_ACCESS",
        40: "MAINTAINER_ACCESS",
        50: "OWNER_ACCESS",
    }
    grouped_members = []
    for group in group_list:
        for member in group.members_all.list(all=True):
            grouped_members.append(
                {
                    "name": member.name,
                    "username": member.username,
                    "locked": member.locked,
                    "state": member.state,
                    "group_id": member.group_id,
                    "id": member.id,
                    "access_level": ACCESS_LEVELS.get(member.access_level),
                }
            )
    return grouped_members


def get_projects():
    """https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html"""
    all_projects = []
    for project in list(
        gl.projects.list(membership=True, get_all=True)
    ):  # Are you a member of all projects?
        all_projects.append(
            {
                "project": project.name,
                "path": project.path_with_namespace,
                "url": project.web_url,
                "id": project.id,
                "archived": project.archived,
            }
        )
    return all_projects


def get_ldap_groups():
    ldap_groups = []
    for group in gl.ldapgroups.list(get_all=True):
        ldap_groups.append(
            {
                "provider": group.provider,
                "group_access": group.group_access,
                "cn": group.cn,
            }
        )
    return ldap_groups


def get_saml_groups(group_list):
    saml_groups = []
    for group in group_list:
        for saml_group in group.saml_group_links.list(get_all=True):
            saml_groups.append(
                {
                    "saml_group_name": saml_group.saml_group_name,
                    "access_level": saml_group.access_level,
                }
            )
    return saml_groups


def to_csv(filename, arr, keys=None):
    # Open a new CSV file for writing
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        if not keys:
            fieldnames = arr[0].keys()
        else:
            fieldnames = keys
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(arr)


gl = authenticate()

group_list = gl.groups.list(all=True)

all_groups = get_groups(group_list)
to_csv(f"{script_dir}/groups_{now}.csv", all_groups)

all_projects = get_projects()
to_csv(f"{script_dir}/projects_{now}.csv", all_projects)

all_members = get_members()
to_csv(f"{script_dir}/members_{now}.csv", all_members)

grouped_members = get_members_by_group(group_list)
to_csv(f"{script_dir}/grouped_members_{now}.csv", grouped_members)

"""
These require some higher permissions and just fails and continues if you do not have access.
This data could be supplimental.
"""

try:
    ldap_groups = get_ldap_groups()
    to_csv(f"{script_dir}/ldap_groups_{now}.csv", ldap_groups)
except gitlab.exceptions.GitlabListError as e:
    print("Unable to test without an ldap setup")
    # raise e

try:
    saml_groups = get_saml_groups(group_list)
    to_csv(f"{script_dir}/saml_groups_{now}.csv", saml_groups)
except gitlab.exceptions.GitlabListError as e:
    print("Unable to test without an ldap setup")
    # raise e
