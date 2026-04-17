# https://python-gitlab.readthedocs.io/en/stable/index.html

import json
import csv
import logging
import os
from datetime import datetime as dt
from pathlib import Path

# pip install python-gitlab
import gitlab
import gitlab.exceptions
from gitlab.exceptions import (
    GitlabAuthenticationError,
    GitlabHttpError,
    GitlabListError,
)

# pip install python-dotenv
from dotenv import load_dotenv

# pip install requests
import requests
from requests.packages import urllib3

enable_public_gitlab_settings = True

script_dir = f"{Path(__file__).resolve().parent}/logs"  # directory of this script
date_time_format_w_seconds = "%Y-%m-%d_%H-%M-%S"
now = dt.now().strftime(date_time_format_w_seconds)
log_file_name = f"{script_dir}/output_{now}.log"

ACCESS_LEVELS = {
    0: "NO_ACCESS",
    5: "MINIMAL_ACCESS",
    10: "GUEST_ACCESS",
    20: "REPORTER_ACCESS",
    30: "DEVELOPER_ACCESS",
    40: "MAINTAINER_ACCESS",
    50: "OWNER_ACCESS",
}

# https://docs.gitlab.com/api/rest/#offset-based-pagination
# By documentation this is the upper limit applied to all.
# It will use this when it automates the pagination
per_page = 100

# Create a console handler
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def http_logging():
    """
    This is to get the deep debugging info out of the gitlab module
    for http request traffic. A recommended logging config.
    """
    # Define a formatter for the log messages
    formatter = logging.Formatter(
        "%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s"
    )

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.DEBUG)
    urllib3_logger_handler = logging.FileHandler(log_file_name)
    urllib3_logger_handler.setLevel(logging.DEBUG)
    urllib3_logger_handler.setFormatter(formatter)
    urllib3_logger.addHandler(urllib3_logger_handler)
    urllib3_logger.addHandler(console_handler)
    urllib3_logger.propagate = True
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Python312\Lib\site-packages\gitlab\_backends\requests_backend.py
    # Python312\Lib\site-packages\requests\sessions.py
    gitlab_logger = logging.getLogger("python-gitlab")
    gitlab_logger.setLevel(logging.DEBUG)
    gitlab_logger_handler = logging.FileHandler(log_file_name)
    gitlab_logger_handler.setLevel(logging.DEBUG)
    gitlab_logger_handler.setFormatter(formatter)
    gitlab_logger.addHandler(gitlab_logger_handler)
    gitlab_logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_handler = logging.FileHandler(log_file_name)
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(console_handler)

    logger.info(msg=f"{log_file_name = }")
    return logger


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
        logger.info(f"Successfully connected to GitLab at {GITLAB_URL}")
        logger.info("... running ...")
        return gl
    except GitlabAuthenticationError as e:
        logger.info(f"Error connecting to GitLab: {e}")
        raise e


def get_groups(all_group_objects):
    """https://python-gitlab.readthedocs.io/en/stable/gl_objects/groups.html"""
    all_groups = []
    for group in all_group_objects:
        all_groups.append(
            {
                "url": group.web_url,
                "name": group.full_path,
                "archived": getattr(group, "archived", None),
                "id": group.id,
                "ldap_access": ACCESS_LEVELS.get(getattr(group, "ldap_access", None)),
                "ldap_cn": getattr(group, "ldap_cn", None),
            }
        )
    return all_groups


def get_members(gl):
    # https://docs.gitlab.com/api/users/
    all_members = []
    kwargs = {"iterator": True, "per_page": per_page}
    if enable_public_gitlab_settings:
        kwargs["timeout"] = 2

    for member in list(gl.users.list(**kwargs)):
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

    grouped_members = []
    for group in group_list:
        try:
            for member in group.members_all.list(all=True, per_page=per_page):
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
        except GitlabListError as e:
            if e.response_code == 403:
                logger.error(
                    f"You don't have permission to get the membership info of group {group.name}",
                )
    return grouped_members


def get_projects(all_projects):
    """https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html"""
    parsed_projects = []
    for project in all_projects:
        parsed_projects.append(
            {
                "project": project.get("name"),
                "path": project.get("path_with_namespace"),
                "url": project.get("web_url"),
                "id": project.get("id"),
                "archived": project.get("archived"),
            }
        )
    return parsed_projects


def get_ldap_groups(gl):
    ldap_groups = []
    for ldap in list(gl.ldapgroups.list(get_all=True, per_page=per_page)):
        ldap_groups.append(json.loads(ldap.to_json()))
    return ldap_groups


def get_saml_groups(group_list):
    saml_groups = []
    for group in group_list:
        for saml_group in list(
            group.saml_group_links.list(get_all=True, per_page=per_page)
        ):
            saml_groups.append(json.loads(saml_group.to_json()))
    return saml_groups


def to_csv(filename, arr, keys=None):
    if not arr:
        raise IndexError("Empty array")
    # Open a new CSV file for writing
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = keys
        if not keys:
            fieldnames = arr[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(arr)


def to_json(filename, arr):
    if not arr:
        raise IndexError("Empty array")
    with open(filename, "w", newline="", encoding="utf-8") as jsonfile:
        json.dump(arr, jsonfile, indent=4)


def get_projects_json(gl):
    """https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html"""
    project_list = []
    membership = enable_public_gitlab_settings
    for project in list(
        gl.projects.list(membership=membership, iterator=True, per_page=per_page)
    ):
        project_list.append(json.loads(project.to_json()))
    return project_list


if __name__ == "__main__":
    os.makedirs(script_dir, exist_ok=True)
    logger = http_logging()

    gl = authenticate()

    """
    Since I'm testing against GitLab saas these requests will return 
    all public data hosted on GitLab which is causing timeouts and errors so when I
    run it I'll check this setting to adjust accordingly. By default this is made
    for a private GitLab organization.
    """
    enable_public_gitlab_settings = "jumiles@paloaltonetworks.com" in gl.user.email

    """
    https://docs.gitlab.com/api/groups/#list-all-groups
    This library wraps the gitlab api referenced here.
    See this documentation page section for 'active', archived' and 'all_available'
    ...'all' is a python-gitlab specific parameter that likely is the same as all_available
    """
    try:
        group_list = gl.groups.list(
            all=True,
            active=True,
            archived=False,
            all_available=not enable_public_gitlab_settings,
            owned=False,
        )
    except gitlab.exceptions.GitlabListError as e:
        if e.response_code == 500:
            logger.error(
                "Justin get a 500 on this since it tries to get all public gitlab.com repos, which is a lot and probably internally blocked on the SaaS."
            )

    all_groups = get_groups(group_list)
    to_csv(f"{script_dir}/groups_{now}.csv", all_groups)

    all_projects = get_projects_json(gl)
    to_json(f"{script_dir}/projects_{now}.json", all_projects)

    all_projects = get_projects(all_projects)
    to_csv(f"{script_dir}/projects_{now}.csv", all_projects)

    try:
        all_members = get_members(gl)
        to_csv(f"{script_dir}/members_{now}.csv", all_members)
    except requests.exceptions.ReadTimeout as e:
        logger.error("Justin gets timeouts on this")
        # logger.error(e)

    try:
        grouped_members = get_members_by_group(group_list)
        to_csv(f"{script_dir}/grouped_members_{now}.csv", grouped_members)
    except GitlabHttpError as e:
        if e.response_code == 403:
            logger.error(e)
        else:
            raise e
    except gitlab.exceptions.GitlabListError as e:
        if e.response_code == 403:
            logger.error(e)
        else:
            raise e

    """
    These require some higher permissions and just fails and continues if you do not have access.
    This data could be supplimental.
    """
    try:
        ldap_groups = get_ldap_groups(gl)
        to_json(f"{script_dir}/ldap_groups_{now}.json", ldap_groups)
    except gitlab.exceptions.GitlabListError as e:
        logger.error(e)

    try:
        saml_groups = get_saml_groups(group_list)
        to_json(f"{script_dir}/saml_groups_{now}.json", saml_groups)
    except gitlab.exceptions.GitlabListError as e:
        logger.error(e)
    except gitlab.exceptions.GitlabAuthenticationError as e:
        logger.error(e)

    logger.info(f"Files and logs at {script_dir} with timestamp {now}")
