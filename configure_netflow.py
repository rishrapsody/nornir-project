from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
import ipdb
from pprint import pprint
import logging

nr = InitNornir(config_file="config.yml")

def get_int(task):
    output = task.run(task=send_command, command="show ip interface brief",severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()

    int_list = []
    for key,value in task.host["facts"]["interface"].items():
        if value["ip_address"] != "unassigned":
            int_list.append(key)


    for intf in int_list:
        task.run(task=send_configs, configs=["ip flow-export destination 192.168.1.19 2055","ip flow-export version 9","interface {}".format(intf),"ip route-cache flow","exit"], severity_level=logging.DEBUG)

lab_filter = nr.filter(F(group__contains='lab'))
results = lab_filter.run(task=get_int)
print_result(results)
#ipdb.set_trace()
