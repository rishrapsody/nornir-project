from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
from pytest_check import check_func
import ipdb

@check_func
def check_intf(task):
    result = task.run(task=send_command, command="show version")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
#    print("Device {} has {} Fa Interfaces".format({task.host},task.host["facts"]["version"]["number_of_intfs"]['FastEthernet']))
    data = int(task.host["facts"]["version"]["number_of_intfs"]['FastEthernet'])
    try:
        assert data == 4, f"{task.host} FAILED"
    except Exception:
        pass




def test_intf(nr):
    devices = nr.filter(F(groups__contains='lab'))
    devices.run(task=check_intf)
