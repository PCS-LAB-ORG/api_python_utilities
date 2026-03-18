#!/python

# from apu.utils import login

# login.login()

from apu.yor import get_tags


def test_get_tags(auth_token):
    tags = get_tags.get_tags()
    for tag in tags:
        print(tag["name"])
    assert not len(tags) == 0
