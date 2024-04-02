from .util.util import get_ansible

testinfra_runner, testinfra_hosts = get_ansible()


def test_always_fail():
    assert False
