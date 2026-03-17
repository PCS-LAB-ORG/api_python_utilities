#!/python

import pytest

# from apu.utils import login, http_logging # importing this should trigger the login procedure

from apu.utils import login

login.login()

from apu.yor import get_tags

def my_test():
    tags = get_tags.get_tags()
    for tag in tags:
        print(tag['name'])
    return len(tags)