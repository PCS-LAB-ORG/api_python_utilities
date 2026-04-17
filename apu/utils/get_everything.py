"""
This is to build a big json file of all 'gettable' data.

Generally I'd use this to look at patterns and try and derive mappings.

This is not meant to be a backup tool.
"""

from datetime import datetime, timedelta
import os
import time
import json
from pathlib import Path
from typing import Callable

from apu.repositories import get_repo as repos
from apu.roles import core as roles
from apu.users import core as users
from apu.permissions import get_all_permission_groups as permissions
from apu.utils import login, constants


def file_stats(filename):
    stats = os.stat(filename)
    print(f"File Size: {stats.st_size} bytes")
    print(f"Last Modified: {time.ctime(stats.st_mtime)}")
    print(f"Last Accessed: {time.ctime(stats.st_atime)}")
    print(f"Creation Time: {time.ctime(stats.st_birthtime)}")
    print(f"Permissions: {oct(stats.st_mode)}")


data = {}

now = datetime.now()
cache_file_name = f"{constants.script_dir}/cache.json"

if Path.exists(cache_file_name):
    file_stats(cache_file_name)
    # Open the file and load the data
    with open(cache_file_name, "r+") as file:
        data = json.load(file)

after_invalidate_datetime = timedelta(minutes="10")


def cache_invalid(data_obj):
    return (
        data_obj in data
        and "time" in data[data_obj]
        and now - data[data_obj]["time"] > after_invalidate_datetime
    )


def try_update(data_obj, fn: Callable):
    if cache_invalid(data_obj):
        data[data_obj] = {
            "time": now,
            "data": fn(),
        }


login.login()

try_update("repositories", repos.get_vcs_repository_page())
try_update("roles", roles.list_roles())
try_update("users", users.get())
try_update("permissions", permissions.get())


with open(cache_file_name, "w+", newline="") as cache_file:
    json.dump(data, cache_file, indent=4)
# pprint.pprint(data)
file_stats(cache_file_name)
