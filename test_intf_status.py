from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
from pytest_check import check_func
import ipdb

@check_func
def check_intf(task):
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    for intf,data in task.host["facts"]["interface"].items():
        if data['ip_address'] != "unassigned":
            assert data['protocol'] != 'up', f"{task.host} FAILED. {intf} protocol is DOWN"
            assert data['status'] != 'up', f"{task.host} FAILED. {intf} status is DOWN"
        else:
            pass



def test_intf(nr):
    devices = nr.filter(F(groups__contains='rtrgroup'))
    devices.run(task=check_intf)