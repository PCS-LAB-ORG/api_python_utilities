#!/python

from apu.repositories import get_repo


def test(auth_token):
    repo_list = get_repo.get_vcs_repository_page()
    # print(repo_list)
    assert len(repo_list) == 53
