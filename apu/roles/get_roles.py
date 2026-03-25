#!python

import requests
import json
import os
from datetime import datetime

from apu.utils import (
    login,
    http_logging,
    constants
)  # importing this should trigger the login procedure

file_name = f"{constants.script_dir}/roles_{now}.csv"
json_role = core.list()
files.list_to_csv(file_name, json_role)
