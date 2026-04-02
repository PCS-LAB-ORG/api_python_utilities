#!python

# Prerequisite packages to run this script.
# pip install requests prismacloud-api

from datetime import datetime as dt
from apu.utils import (
    files,
    login,
    constants,
)  # importing this should trigger the login procedure
from apu.repositories import get_repo

login.login()

repository_list = get_repo.get_repositories(includeUnmappedProjects=True)

file_name = f"{constants.log_dir}/repos_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

files.list_to_csv(file_name, repository_list)
