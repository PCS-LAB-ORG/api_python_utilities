#!python

# Prerequisite packages to run this script.
# pip install requests prismacloud-api

import os
from datetime import datetime as dt
from apu.utils import files  # importing this should trigger the login procedure
from apu.repositories import get_repo

repository_list = get_repo.get_repositories(includeUnmappedProjects=True)

file_name = f"{os.getcwd()}/repos_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

files.list_to_csv(file_name, repository_list)
