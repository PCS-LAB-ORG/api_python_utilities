#!python

# Prerequisite packages to run this script.
# pip install requests prismacloud-api

import os
import csv
import json
import requests
from datetime import datetime as dt
from apu.utils import login, files  # importing this should trigger the login procedure

repository_list = get_repo.get_repositories(includeUnmappedProjects=True)

file_name = f"{os.getcwd()}/repos_{dt.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

files.list_to_csv(file_name, repository_list)
