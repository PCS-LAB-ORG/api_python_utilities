#!python


from apu.access_keys import simple_rotate


def test_simple_rotate_no_del(auth_token):
    key = {}
    simple_rotate.rotate_key(key)

# def test_simple_rotate_del():
#     key = {}
#     simple_rotate.rotate_key(key, allow_delete=True)

# @pytest.mark.skip(reason="this test is currently disabled")
def test_assert():
    assert True

def test_rotate_expired_key():
    pass