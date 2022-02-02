from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
import pytest
from nornir import InitNornir
import ipdb

nr = InitNornir(config_file="config.yml")


def get_intf_status(task):
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["raw_data"] = result.scrapli_response.genie_parse_output()


def get_names():
    devices = nr.filter(F(groups__contains='lab')).inventory.hosts.keys()
    return devices


class TestVersionCheck:

    @pytest.fixture(scope="class", autouse=True)
    def setup_teardown(self,pytestnr):
        devices = pytestnr.filter(F(groups__contains='lab'))
        devices.run(task=get_intf_status)
        yield
        for host in devices.inventory.hosts.values():
            host.data.pop("raw_data")

    @pytest.mark.parametrize(
        'device_name', get_names()
    )

    def test_up_status_intf(self, pytestnr, device_name):
        nr_host = pytestnr.inventory.hosts[device_name]
        intf_count = 0
        up_count = 0
        for intf, data in nr_host["raw_data"]["interface"].items():
            if data['ip_address'] != "unassigned":
                intf_count = intf_count + 1
                if data['protocol'] = 'up' and data['status'] == 'up':
                    up_count = up_count + 1
        assert intf_count == up_count, f"{nr_host} FAILED. Intf in UP status:{up_count} does not match configured Intf:{intf_count}"

