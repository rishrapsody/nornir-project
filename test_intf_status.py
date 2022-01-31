from nornir_scrapli.tasks import send_command
from nornir.core.filter import F
from pytest_check import check_func
import ipdb

@check_func
def check_intf(task):
    my_list = []
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
#    print(task.host["facts"])
    for intf,data in task.host["facts"]["interface"].items():
        if data['ip_address'] != "unassigned":
            if data['protocol'] == 'up':
                my_list.append(data['protocol'])
                if data['status'] == 'up':
                    my_list.append(data['protocol'])
        assert len(my_list) == 2, f"{task.host} Failed"
#            print("iam here")
#            print("Device {} interface {} Protocol is {}".format(task.host,intf,data['protocol']))
#            assert data['protocol'] == 'down', f"{task.host} FAILED. {intf} protocol is DOWN"
#            assert data['status'] == 'up', f"{task.host} FAILED. {intf} status is DOWN"




def test_intf(nr):
#    devices = nr.filter(F(groups__contains='rtrgroup'))
    nr.run(task=check_intf)