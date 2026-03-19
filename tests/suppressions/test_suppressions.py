#!/python

# from apu.utils import login

# login.login()

from apu.suppressions import core


def test_get(auth_token):
    suppression_list = core.get()
    for suppression in suppression_list:
        print(
            f"{suppression["suppressionType"]} {suppression["policyId"]} {suppression["comment"]}"
        )
    assert not len(suppression_list) == 0
