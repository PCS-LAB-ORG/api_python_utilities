#!python


from apu.utils import (
    constants,
    files,
    login,
)  # importing this should trigger the login procedure
from apu.roles import core

login.login()
file_name = f"{constants.script_dir}/roles_{constants.now}.csv"
# json_role = core.list_roles()
json_role = core.special_list_roles()

files.obj_to_csv(file_name, json_role)
