from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
import ipdb
from pprint import pprint
import logging
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from nornir.core.filter import F
from ipaddress import IPv4Address

nr = InitNornir(config_file="config.yml")
global_list = []

def get_net(task):
    if task.host.platform == 'ios':
        ios_list = get_net_ios(task)
        global_list.append(ios_list)
        print(global_list)
    elif task.host.platform == 'iosxr':
        find_ip_iosxr(task)
    elif task.host.platform == 'nxos':
        find_ip_nxos(task)
    else:
        find_ip_junos(task)

def get_net_ios(task):
    output = task.run(task=send_command, command="show ip int brief", severity_level=logging.DEBUG)
    task.host["facts"] = output.scrapli_response.genie_parse_output()
#    print(task.host)
#    pprint(task.host["facts"])
    sub_list = []
#    print(task.host["facts"]["interface"].items())
    for key,value in task.host["facts"]["interface"].items():
#        print(value)
        if value["ip_address"] != "unassigned":
            sub_list.append(value["ip_address"])
        else:
            pass
    print(f"list for {task.host} is " + sub_list)
    return(sub_list)




#devices = nr.filter(F(groups__contains='cloud'))
results = nr.run(task=get_net)