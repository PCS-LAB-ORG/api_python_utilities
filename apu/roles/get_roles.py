#!python


from apu.utils import (
    login,
    http_logging,
    constants,
    files
)  # importing this should trigger the login procedure
from apu.roles import core

file_name = f"{constants.script_dir}/roles_{constants.now}.csv"
json_role = core.list()
files.list_to_csv(file_name, json_role)
