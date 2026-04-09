import json
import requests

from prismacloud.api import pc_api

from apu.utils import files, login
from apu.utils import core


def get():
    # Get user list
    url = f"{login.settings['url']}/v3/user"
    response = requests.request("GET", url, headers=login.headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            quit(response.text)

    user_list = json.loads(response.text)
    return user_list


def create(
    user={},
    accessKeysAllowed=True,
    activeRole={},
    defaultRoleId=None,
    email=None,
    firstName=None,
    lastName=None,
    roleIds=None,
    timeZone=None,
):
    """https://pan.dev/prisma-cloud/api/cspm/add-user-v-2/"""
    # Expected format. See API def in pan.dev
    user_attr = {
        "accessKeysAllowed": bool(accessKeysAllowed),
        "activeRole": activeRole,
        "defaultRoleId": defaultRoleId,
        "email": email,
        "firstName": firstName,
        "lastName": lastName,
        "roleIds": roleIds.replace(" ", ", "),
        "timeZone": timeZone,
    }
    user.update(user_attr)
    payload = json.dumps(user)
    res = pc_api.user_create(payload)
    print(f"Create User ({user['email']}) response code: {res}")
    return res


def create_from_user_csv(file_name):
    for user in files.read_csv(file_name):
        core.create_user(user)


def enable_disable_user(username, enable=True):
    """
    Set user status enabled/disabled.
    https://pan.dev/prisma-cloud/api/cspm/update-user-profile/
    https://live.paloaltonetworks.com/t5/general-topics/disable-user/td-p/207822

    This script receives 200 code even if the status is unchanged.
    """
    # WARNING this username field supports regex. I'd recommend always being very explicit or searching for users
    # with the same string.
    username = ""  # Use to toggle status. Documented as email but, username handles service accounts and users
    enable = str(enable).lower()

    url = f"{login.settings['url']}/user/{username}/status/{enable}"
    payload = {}

    response = requests.request("PATCH", url, headers=login.headers, data=payload)
    response.raise_for_status()
    print(response)
