from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
from pytest_check import check_func
import ipdb

@check_func
def check_intf(task):
    result = task.run(task=send_command, command="show ip interface brief")
    task.hosts["facts"] = result.scrapli_response.genie_parse_output()
    ipdb.set_trace()



def test_intf(nr):
    devices = nr.filter(F(groups__contains='rtrgroup'))
    devices.run(task=check_intf)