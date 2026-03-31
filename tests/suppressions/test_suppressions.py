#!/python

import pytest

from apu.suppressions import core


# as documented
# pylint: disable=unused-argument
def test_get(auth_token):
    with pytest.raises(FileNotFoundError):
        suppression_list = core.get()
        for suppression in suppression_list:
            print(
                f"{suppression["suppressionType"]} {suppression["policyId"]} {suppression["comment"]}"
            )
        assert not len(suppression_list) == 0
