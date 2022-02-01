from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
import pytest
from nornir import InitNornir
import ipdb

nr = InitNornir(config_file="config.yml")


def check_intf(task):
    result = task.run(task=send_command, command="show version")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
#    print("Device {} has {} Fa Interfaces".format({task.host},task.host["facts"]["version"]["number_of_intfs"]['FastEthernet']))
 #   data = int(task.host["facts"]["version"]["number_of_intfs"]['FastEthernet'])
#    assert data == 4, f"{task.host} FAILED"

def get_names():
    devices = nr.filter(F(groups__contains='lab')).inventory.hosts.keys()
    return devices


class TestVersion:

    @pytest.fixture(scope="class", autouse=True)
    def setup_teardown(self,pytestnr)
        devices = nr.filter(F(groups__contains='lab'))
        devices.run(task=check_intf)
        yield
        for host in devices.hosts.values():
            host.data.pop("facts")

    @pytest.test.parametrize(
        'device_name', get_names()
    )

    def test_facts(self, pytestnr, device_name):
        nr_host = pytestnr.inventory.hosts[device_name]
        data = int(nr_host["facts"]["version"]["number_of_intfs"]['FastEthernet'])
        assert data == 4, f"{nr_host} FAILED"
