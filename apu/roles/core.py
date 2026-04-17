#!/bin/bash python
# https://pan.dev/prisma-cloud/api/code/sbom-dependencies/

# Prerequisite packages to run this script.
# pip install pprintpp requests prismacloud-api
import json
from dataclasses import dataclass
from dacite import from_dict
import requests
from prismacloud.api import pc_api

from apu.utils import login  # importing this should trigger the login procedure


@dataclass
class role:
    id: str
    name: str
    description: str | None
    lastModifiedBy: str
    lastModifiedTs: int
    accountGroupIds: list[str]
    resourceListIds: list[str]
    codeRepositoryIds: list[str]
    associatedUsers: list
    restrictDismissalAccess: bool
    additionalAttributes: dict[str, bool]
    accountGroups: list[dict]
    resourceLists: list[dict]
    codeRepositories: list[dict[str, str]]
    roleType: str
    permissionGroup: str | None = None


def list_roles(role=None):
    url = f"{login.settings['url']}/user/role"

    response = requests.request("GET", url, headers=login.headers)
    response.raise_for_status()
    role_list = json.loads(response.text)
    if not role:
        return role_list
    else:
        for r in role_list:
            if role.get("name") == r.get("name"):
                return r
    # files.list_to_csv(file_name, json_role)


def update_user(user, user_dict=None):
    if user_dict:
        user.update(user_dict)
    pc_api.user_update(user)
    return user


def special_list_roles():
    url = f"{login.settings['url']}/user/role"

    response = requests.request("GET", url, headers=login.headers)
    response.raise_for_status()
    role_list = json.loads(response.text)
    roles = []
    for js_role in role_list:
        roles.append(json_to_role(js_role))
    return roles


def json_to_role(data=None):
    return from_dict(data_class=role, data=data)


if __name__ == "__main__":
    login.login()
    print(special_list_roles())
